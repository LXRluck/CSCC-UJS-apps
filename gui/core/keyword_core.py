"""
Copyright (c) 2015 Letian Sun
Copyright (c) 2025 Xiangrui Li / CSCC-UJS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import re
import jieba
import jieba.analyse as analyse
from PySide6.QtCore import QObject, Signal

jieba.setLogLevel(logging.CRITICAL)

class keyword_abstract(QObject):
    progress = Signal(str, int)# 进度信息：状态+百分比
    finished = Signal(bool, str)# 完成信息：是否成功+信息

    def __init__(self, srt_path):
        """初始化"""
        super().__init__()
        self.srt_path = srt_path
        self.isrunning = True
        
        self.subtitle_text=""
        self.keywords = []

    def extract_subtitle_text(self):
        """提取SRT文件中的纯字幕文本（过滤序号、时间轴、格式符号）"""
        try:
            self.progress.emit("正在读取SRT文件：", 10)
            with open(self.srt_path, "r", encoding="utf-8") as f:
                srt_content = f.read()

            # 1. 移除SRT格式的序号（纯数字行）
            srt_content = re.sub(r'^\d+$', '', srt_content, flags=re.MULTILINE)
            # 2. 移除时间轴（格式：00:00:00,000 --> 00:00:00,000）
            srt_content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', srt_content)
            # 3. 移除HTML标签（如<u>、<i>等）
            srt_content = re.sub(r'<.*?>', '', srt_content)
            # 4. 移除多余空行和空格
            lines = [line.strip() for line in srt_content.split('\n') if line.strip()]
            # 合并为纯文本
            self.subtitle_text = '\n'.join(lines)
            self.progress.emit("提取纯文本完成：", 30)
            return self.subtitle_text

        except Exception as e:
            self.finished.emit(False, f"提取纯文本失败：{str(e)}")
            raise

    def keyword_abstract(self):
        """提取关键字"""
        try:
            self.extract_subtitle_text()
            self.progress.emit("正在为您提取关键字：", 20)
            self.isrunning = True
            # 使用TFIDF算法,提取关键字
            self.keywords = analyse.tfidf(self.subtitle_text, topK = 4)
            self.progress.emit("正在为您提取关键字：", 50)
        except Exception as e:
            self.finished(False, f"提取失败：{str(e)}")
            raise
    
    def run(self):
        # 先初始化
        self.__init__()
                   
        # 提取关键字
        self.keyword_abstract()

    def stop(self):
        self.isrunning = False
        self.progress.emit("正在取消提取：", 0)