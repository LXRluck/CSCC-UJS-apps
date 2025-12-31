import os
import re
import tempfile
from datetime import timedelta
script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
import mpv
import time

class MPVPlayerCore:
    def __init__(self):
        self.mpv_player = mpv.MPV(
            vo='gpu',  
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True, 
            # SUBTITLE OPTIONS
            sid='no',
            sub_auto='no',
            sub_font_size=24,
            sub_color='#FFFFFF',
            sub_border_color='#000000',
            sub_border_size=2
        )

        self.is_playing = False
        self.current_file = None

        self.set_volume(80)

        self.injected_subtitle_ids = []
        self.temp_subtitle_files = []
        self.temp_sub_track_id=None

        self.duration_loaded = False

        @self.mpv_player.event_callback('file-loaded')
        def on_file_loaded(event):
            self.duration_loaded = True

        self.progress_update_callback=None

        @self.mpv_player.property_observer('time-pos')
        def time_pos_observer(_name, value):
            #进度监听回调
            if self.progress_update_callback and value is not None:
                self.progress_update_callback(value, self.get_duration())

    def bind_to_window(self, win_id):
        #将MPV绑定到指定窗口
        self.mpv_player.wid = str(int(win_id))

    def load_video(self, file_path):
        #加载并播放指定视频文件
        self.stop()
        self.current_file = file_path
        self.duration_loaded= False
        self.mpv_player.play(file_path)
        self.is_playing = True

    def toggle_play_pause(self):
        #切换播放/暂停状态
        if not self.current_file:
            raise ValueError("未加载视频文件")
        
        if self.is_playing:
            self.mpv_player.pause=True
            self.is_playing = False
        else:
            self.mpv_player.pause=False
            self.is_playing = True

    def stop(self):
        #停止播放并重置状态
        if self.current_file:
            self.mpv_player.stop()
            self.is_playing = False
            self.current_file = None
            # 清理所有临时字幕轨道
            for sub_id in self.injected_subtitle_ids:
                try:
                    self.mpv_player.command("sub-remove", sub_id)
                except:
                    pass
            self.injected_subtitle_ids.clear()
            # 清理所有临时字幕文件
            for temp_file in self.temp_subtitle_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
            self.temp_subtitle_files.clear()
            if self.temp_sub_track_id is not None:
                self.mpv_player.command('sub-remove', self.temp_sub_track_id)
                self.temp_sub_track_id = None
    def set_volume(self, value):
        if 0 <= value <= 100:
            self.mpv_player.volume = value

    def get_volume(self):
        return self.mpv_player.volume

    def get_duration(self, timeout=5.0, interval=0.1):
        #获取总时长
        start = time.time()
        while time.time() - start < timeout:
            if self.duration_loaded:
                try:
                    return self.mpv_player.duration or 0
                except AttributeError:
                    return 0
            time.sleep(interval)
        return 0
    
    def set_position(self, seconds):
        if 0 <= seconds <= self.get_duration():
            self.mpv_player.seek(seconds, reference='absolute')

    def get_position(self):
        try:
            return self.mpv_player.time_pos or 0
        except:
            return 0

    def set_progress_callback(self, callback):
        #进度更新回调
        self.progress_update_callback = callback

    def set_subtitle_file(self, subtitle_path):
        subtitle_path = os.path.abspath(subtitle_path)
        if not os.path.exists(subtitle_path):
            raise FileNotFoundError(f"字幕文件不存在：{subtitle_path}")
    
        #清除所有旧字幕轨道
        self._cleanup_all_subtitles()
    
        try:
            self.mpv_player.sid = "no"  # 禁用内置字幕
            self.mpv_player.sub_auto = "no"  # 关闭自动匹配
            self.mpv_player.sub_codepage = "utf-8"  # 强制指定编码（兼容绝大多数字幕）
        
            self.mpv_player.command("sub-add", subtitle_path)
        
            #强制启用新添加的外部字幕轨道
            self.mpv_player.sub = "1" 
            self.mpv_player.sub_visibility = True  
        
            print(f"字幕切换成功：{subtitle_path}")
            print(f"当前启用的字幕轨道：{self.mpv_player.sub}")  
        
        except Exception as e:
            # 捕获MPV命令执行异常（如字幕文件损坏）
            raise RuntimeError(f"切换字幕失败：{str(e)} | 字幕路径：{subtitle_path}")


    def _cleanup_all_subtitles(self):
        # 清除所有注入的字幕轨道
        for sub_id in self.injected_subtitle_ids:
            try:
                self.mpv_player.command("sub-remove", sub_id)
            except Exception as e:
                print(f"清除旧轨道{sub_id}失败：{e}")
        self.injected_subtitle_ids.clear()
    
        for temp_file in self.temp_subtitle_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"删除临时文件{temp_file}失败：{e}")
        self.temp_subtitle_files.clear()
    
        # 清除MPV当前的字幕配置
        self.mpv_player.sub_file = "" 
        self.mpv_player.sub = "0" 
        self.mpv_player.sub_visibility = False 
        
# 实时字幕注入
# ///////////////////////////////////////////////////////////////
    def inject_mpv_subtitle(self, start_time, end_time, subtitle_text):
        """
        实时注入字幕到MPV播放器
        
        Args:
            start_time: 字幕开始时间（秒）
            end_time: 字幕结束时间（秒）
            subtitle_text: 字幕文本内容
        """
        if not isinstance(subtitle_text, str):
            print(f"字幕文本类型错误，要求字符串，实际为：{type(subtitle_text)} | 内容：{subtitle_text}")
            return
        
        if not isinstance(start_time, (int, float)) or not isinstance(end_time, (int, float)):
            print(f"字幕时间类型错误，开始：{type(start_time)} 结束：{type(end_time)}")
            return
        
        subtitle_text = subtitle_text.strip()
        if not subtitle_text or not self.mpv_player:
            return
        
        # 清理旧的字幕轨道
        self._cleanup_old_subtitles()
        
        try:
            # 转换时间为SRT格式 (HH:MM:SS,mmm)
            start_str = self._seconds_to_srt_time(start_time)
            end_str = self._seconds_to_srt_time(end_time)
            
            # 创建临时SRT文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as f:
                srt_content = f"1\n{start_str} --> {end_str}\n{subtitle_text}\n"
                f.write(srt_content)
                temp_file = f.name
            
            try:
                # 使用sub-add命令加载临时字幕文件
                # 直接使用属性设置字幕文件
                self.mpv_player.sub_file = temp_file
                
                # 记录临时文件路径
                self.temp_subtitle_files.append(temp_file)
                
                # 确保字幕可见
                self.mpv_player.sub_visibility = True
                
                # 打印调试信息
                print(f"字幕注入成功：{subtitle_text[:50]}...")
                
            except Exception as cmd_error:
                print(f"字幕设置失败：{cmd_error}")
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
        except Exception as e:
            print(f"字幕注入失败：{type(e).__name__} - {e} | 字幕内容：{subtitle_text[:100]}")
    
    def _cleanup_old_subtitles(self):
        """清理旧的临时字幕轨道，避免堆积"""
        try:
            # 限制最大保留的字幕轨道数量（保留最新的3个）
            while len(self.injected_subtitle_ids) > 3:
                old_sub_id = self.injected_subtitle_ids.pop(0)
                try:
                    self.mpv_player.command("sub-remove", old_sub_id)
                except:
                    pass
            
            # 清理旧的临时字幕文件（保留最新的3个）
            while len(self.temp_subtitle_files) > 3:
                old_file = self.temp_subtitle_files.pop(0)
                try:
                    if os.path.exists(old_file):
                        os.remove(old_file)
                except:
                    pass
        except Exception as e:
            print(f"清理字幕轨道失败：{e}")
    
    def _seconds_to_srt_time(self, seconds):
        """将秒数转换为SRT时间格式 (HH:MM:SS,mmm)"""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def fast_forward(self):
        if not self.current_file:
            raise ValueError("未加载视频文件，无法快进")
    
        total_duration = self.get_duration()
        current_pos = self.get_position()
    
        increment = total_duration * 0.01
        
        if increment <= 0: 
            return

        new_pos = min(current_pos + increment, total_duration)
    
        if increment<5: self.set_position(new_pos+5)
        else: self.set_position(new_pos)

    def fast_rewind(self):
        if not self.current_file:
            raise ValueError("未加载视频文件，无法快退")
    
        total_duration = self.get_duration()
        current_pos = self.get_position()
    
        increment = total_duration * 0.01
        if increment <= 0:
            return

        new_pos = max(current_pos - increment, 0)
        self.set_position(new_pos)

    def cleanup(self):
        self.stop()
        self.mpv_player.terminate()

    def __del__(self):
        self.cleanup()
