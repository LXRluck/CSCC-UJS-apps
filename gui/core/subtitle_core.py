import os
import re
import sys
import time
import tempfile
from PySide6.QtCore import QObject, Signal
from datetime import timedelta
import subprocess
from tqdm import tqdm
from opencc import OpenCC
from funasr import AutoModel

# 清理临时文件工具函数
def clean_temp(files):
    for file in files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception as e:
                print(f"警告：无法删除临时文件 {file}: {e}")

# 分片识别的字幕生成线程
class SubtitleWorker(QObject):
    progress = Signal(str, int)
    finished = Signal(bool, str)
    subtitle_updated = Signal(int, float, float, str)  # 新增：实时更新单条字幕信号

    def __init__(self, model,player_core, video_path, srt_path, total_duration, slice_duration=10, short_segment_threshold=2.0):
        super().__init__()
        self.model = model  # 预加载的FunASR模型
        self.player_core = player_core  # 传入的播放器核心对象
        self.video_path = video_path
        self.srt_path = srt_path  # 修复原代码的元组问题（原代码多了个逗号）
        self.total_duration = total_duration  # 视频总时长
        self.slice_duration = slice_duration  # 音频切片时长（默认10秒）
        self.short_segment_threshold = short_segment_threshold  # 短片段合并阈值（默认2秒）
        self.is_running = True
        self.converter = OpenCC('t2s')  # 繁转简
        self.subtitle_index = 1  # 字幕序号
        self.temp_files = []  # 临时音频文件缓存
        self.short_segments_cache = []  # 短片段缓存（用于合并）

    # 提取指定时间段的音频切片（复用原Whisper的ffmpeg逻辑，保证切片格式统一）
    def extract_audio_slice(self, start_time, duration, output_file):
        cmd = [
            'ffmpeg',
            '-y',  # 覆盖已存在的文件
            '-ss', f'{start_time:.2f}',  # 起始时间
            '-i', self.video_path,  # 输入视频文件
            '-t', f'{duration:.2f}',  # 提取时长
            '-vn',  # 禁用视频流
            '-acodec', 'pcm_s16le',  # 音频编码
            '-ar', '16000',  # 采样率
            '-ac', '1',  # 单声道
            '-f', 'wav',  # 输出格式
            '-hide_banner',  # 隐藏banner信息
            '-loglevel', 'error',  # 仅输出错误信息
            output_file  # 输出文件路径
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8'
            )
        except subprocess.CalledProcessError as e:
            print(f"音频提取失败：{e.stderr}")
            raise Exception(f"ffmpeg提取音频失败：{e.stderr}")

        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            raise Exception(f"音频切片文件生成失败：{output_file}")

    # 合并短片段
    def merge_short_segments(self):
        if not self.short_segments_cache:
            return
        
        merged_start = self.short_segments_cache[0]["start"]
        merged_end = self.short_segments_cache[-1]["end"]
        merged_text = "".join([seg["text"] for seg in self.short_segments_cache])
        
        start_str = self.format_srt_time(merged_start)
        end_str = self.format_srt_time(merged_end)
        
        with open(self.srt_path, "a", encoding="utf-8") as f:
            f.write(f"{self.subtitle_index}\n")
            f.write(f"{start_str} --> {end_str}\n")
            f.write(f"{merged_text}\n\n")
        
        self.subtitle_updated.emit(self.subtitle_index,merged_start, merged_end, merged_text)
        self.player_core.inject_mpv_subtitle(merged_start, merged_end, merged_text, 1)
        self.subtitle_index += 1
        self.short_segments_cache = []

    # 格式化SRT时间
    def format_srt_time(self, seconds):
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    # 单切片音频转字幕
    def slice_audio_to_subtitle(self, audio_path, slice_start_time):
        """
        识别单切片音频，返回带时间偏移的字幕片段
        :param audio_path: 切片音频路径
        :param slice_start_time: 切片在原视频中的起始时间（秒）
        :return: 字幕片段列表 [{"start": 绝对开始时间, "end": 绝对结束时间, "text": 文本}, ...]
        """
        # 调用FunASR识别切片音频
        res = self.model.generate(
            input=audio_path,
            batch_size_s=30,
            merge_vad=True,
            use_itn=True,
            add_pause=True,
            predict_timestamp=True
        )

        segments = []
        try:
            full_text = res[0].get("text", "").strip()
            timestamps_ms = res[0].get("timestamp", [])
            
            if not full_text or not timestamps_ms:
                return segments
            
            # 按标点拆分文本
            text_segments = self.split_text_by_punctuation(full_text)
            
            # 适配文本和时间戳数量
            if len(text_segments) > len(timestamps_ms):
                text_segments = text_segments[:len(timestamps_ms)]
            elif len(text_segments) < len(timestamps_ms):
                ts_per_segment = len(timestamps_ms) // len(text_segments)
                remainder = len(timestamps_ms) % len(text_segments)
                new_timestamps = []
                current = 0
                for i in range(len(text_segments)):
                    count = ts_per_segment + (1 if i < remainder else 0)
                    count = min(count, len(timestamps_ms) - current)
                    start_ms = timestamps_ms[current][0]
                    end_ms = timestamps_ms[current + count - 1][1]
                    new_timestamps.append([start_ms, end_ms])
                    current += count
                timestamps_ms = new_timestamps
            
            # 转换为绝对时间
            for i in range(min(len(text_segments), len(timestamps_ms))):
                start_ms, end_ms = timestamps_ms[i]
                # 切片内相对时间转秒 + 切片起始时间 = 绝对时间
                seg_start = slice_start_time + (start_ms / 1000.0)
                seg_end = slice_start_time + (end_ms / 1000.0)
                text = self.converter.convert(text_segments[i].strip())  # 繁转简
                
                if text and seg_start < seg_end:
                    segments.append({
                        "start": seg_start,
                        "end": seg_end,
                        "text": text
                    })
        except Exception as e:
            print(f"切片识别失败（兜底处理）：{e}")
            # 给切片一个默认的整段字幕
            full_text = res[0].get("text", "").strip() if res else ""
            if full_text:
                segments.append({
                    "start": slice_start_time,
                    "end": slice_start_time + self.slice_duration,
                    "text": self.converter.convert(full_text)
                })
        return segments

    # 按标点拆分文本
    def split_text_by_punctuation(self, text, split_chars=None):
        if split_chars is None:
            split_chars = r'，。！？；：、.?!;:'
        parts = re.split(f'([{split_chars}])', text)
        merged_parts = []
        temp = ""
        for part in parts:
            if part:
                temp += part
                if part in split_chars:
                    merged_parts.append(temp.strip())
                    temp = ""
        if temp:
            merged_parts.append(temp.strip())
        return merged_parts

    # 核心运行逻辑
    def run(self):
        try:
            if not self.total_duration or self.total_duration <= 0:
                raise Exception("无法获取视频时长")

            # 清空SRT文件
            with open(self.srt_path, "w", encoding="utf-8") as f:
                f.write("")

            current_time = 0  # 当前切片起始时间
            self.progress.emit("开始分片生成字幕...", 10)
            
            total_slices = int(self.total_duration / self.slice_duration) + 1
            
            with tqdm(total=total_slices, desc="字幕生成", unit="切片", ncols=100, file=sys.stdout, position=0) as pbar:
                while current_time < self.total_duration and self.is_running:
                    # 计算进度百分比
                    progress_percent = int(10 + (current_time / self.total_duration) * 90)
                    self.progress.emit(
                        f"正在识别 {current_time:.1f} - {current_time + self.slice_duration:.1f} 秒...", 
                        progress_percent
                    )

                    # 创建临时音频切片文件
                    temp_fd, temp_audio = tempfile.mkstemp(suffix=".wav")
                    os.close(temp_fd)
                    self.temp_files.append(temp_audio)

                    # 提取当前切片的音频
                    self.extract_audio_slice(current_time, self.slice_duration, temp_audio)

                    # 识别当前切片音频
                    slice_segments = self.slice_audio_to_subtitle(temp_audio, current_time)


                    # 处理识别结果
                    for seg in slice_segments:
                        seg_duration = seg["end"] - seg["start"]
                        # 短片段：加入缓存
                        if seg_duration < self.short_segment_threshold:
                            self.short_segments_cache.append(seg)
                        # 长片段：先合并缓存，再写入当前片段
                        else:
                            self.merge_short_segments()
                            start_str = self.format_srt_time(seg["start"])
                            end_str = self.format_srt_time(seg["end"])
                            with open(self.srt_path, "a", encoding="utf-8") as f:
                                f.write(f"{self.subtitle_index}\n")
                                f.write(f"{start_str} --> {end_str}\n")
                                f.write(f"{seg['text']}\n\n")
                            self.subtitle_updated.emit(self.subtitle_index,seg["start"], seg["end"], seg["text"])
                            self.player_core.inject_mpv_subtitle(seg["start"], seg["end"], seg["text"], 1)
                            self.subtitle_index += 1
                            

                    # 切片处理完后，合并缓存中的短片段
                    self.merge_short_segments()

                    # 推进时间轴
                    current_time += self.slice_duration
                    time.sleep(0.1)
                    
                    # 更新进度条
                    pbar.update(1)
                    pbar.set_postfix_str(f"时间: {current_time:.1f}s")

                # 最终合并所有剩余的短片段
                self.merge_short_segments()

                if self.is_running:
                    self.progress.emit("分片字幕生成完成！", 100)
                    self.finished.emit(True, f"字幕已保存：{os.path.basename(self.srt_path)}")
                else:
                    self.finished.emit(False, "用户终止了字幕生成")

        except Exception as e:
            self.finished.emit(False, f"字幕生成失败：{str(e)}")
        finally:
            # 清理临时文件
            clean_temp(self.temp_files)

    # 停止线程
    def stop(self):
        self.is_running = False