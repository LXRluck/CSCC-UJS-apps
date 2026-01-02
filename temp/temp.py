from funasr import AutoModel
import re
import os

print("正在预先加载模型...（首次运行耗时较长，后续复用无需重复加载）")
model = AutoModel(
    model="paraformer-zh",
    vad_model="fsmn-vad",
    punc_model="ct-punc",
    disable_update=True,
    device="cpu",
    model_revision="v2.0.4"
)
print("✅ 模型预先加载完成！")

# ==================== 工具函数 ====================
def format_time(seconds):
    """将秒数格式化为 SRT 字幕时间格式: 00:00:00,000"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

def split_text_by_punctuation(text, split_chars=None):
    """按标点拆分文本，适配时间戳分段"""
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

# ==================== 复用模型生成字幕 ====================
def audio_to_subtitle(preloaded_model, audio_path, output_srt_path=None):

    # 设置默认输出路径
    if output_srt_path is None:
        base_name = os.path.splitext(audio_path)[0]
        output_srt_path = f"{base_name}.srt"
    
    # 复用模型进行推理（无需重新加载）
    print(f"\n正在处理音频: {audio_path}")
    res = preloaded_model.generate(
        input=audio_path,
        batch_size_s=30,
        merge_vad=True,
        use_itn=True,
        add_pause=True,
        predict_timestamp=True
    )
    
    srt_content = []
    index = 1
    try:
        full_text = res[0].get("text", "").strip()
        timestamps_ms = res[0].get("timestamp", [])
        
        if not full_text or not timestamps_ms:
            raise ValueError("未获取到有效文本或时间戳")
        
        # 拆分文本 + 匹配时间戳
        text_segments = split_text_by_punctuation(full_text)
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
        
        # 生成字幕片段
        for i in range(min(len(text_segments), len(timestamps_ms))):
            start_ms, end_ms = timestamps_ms[i]
            start_time = start_ms / 1000.0
            end_time = end_ms / 1000.0
            text = text_segments[i]
            
            if not text or start_time >= end_time:
                continue
            
            start_str = format_time(start_time)
            end_str = format_time(end_time)
            srt_content.extend([str(index), f"{start_str} --> {end_str}", text.strip(), ""])
            index += 1
        
        if index == 1:
            raise ValueError("未生成有效字幕片段")
    
    except Exception as e:
        print(f"⚠️ 解析失败: {e}，启用兜底方案")
        full_text = res[0].get("text", "").strip()
        if full_text:
            srt_content = ["1", "00:00:00,000 --> 00:30:00,000", full_text, ""]
    
    # 写入文件
    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))
    print(f"✅ 字幕生成完成: {output_srt_path}")
    print(f"📝 共生成 {max(index-1, 1)} 条字幕")


# 示例使用
if __name__ == "__main__":
    # 替换为你的音频文件路径
    audio_file = r"D:\video\base_test.mp3"  # 支持 wav, mp3, m4a 等格式
    
    # 生成字幕
    audio_to_subtitle(model,audio_file,r"D:\video\base_test.srt")