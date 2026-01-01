from PySide6.QtCore import QObject, Signal,QThread
from asr3 import ASRClient
from asr2 import SetupPageTools

class asr(QObject):
    progress = Signal(str, int)
    finished = Signal(bool, str)

    def __init__(self, audio_path, model):
        # 初始化
        super().__init__()
        self.audio_path = audio_path
        self.model = model
        self.isrunning = True
        self.asr_client = False

    def asrclient(self):
        try:
            pagetools = SetupPageTools()
            pagetools.current_api_endpoint = "https://api.siliconflow.cn/v1/audio/transcriptions" 
            pagetools.current_api_key = "sk-ghdewvivakkmieipcloffjndnmxsxizoovqsvtkmicklwsdl" 
            pagetools.current_model_name = "TeleAI/TeleSpeechASR" 

            self.progress.emit("开始调用ASR接口...", 50)
            result = pagetools.test_asr_connection(self.audio_path)
            if "错误" not in result:
                self.asr_client = True
            return result
        except Exception as e:
            return f"客户端初始化失败：{str(e)}"
    
    def text_abstract(self):
        if not self.asr_client:
            return "错误：ASR客户端未初始化"
        
        self.progress.emit("正在识别音频内容...", 80)
        try:
            texts = ASRClient.transcribe(self.audio_path, self.model)
            return texts
        except Exception as e:
            self.finished.emit(False, f"识别音频失败: {str(e)}")

    def run(self):
        try:
            self.progress.emit("初始化ASR任务...", 0)
            
            client_result = self.asrclient()
            if "错误" in client_result:
                self.finished.emit(False, client_result)
                return

            abstract_result = self.text_abstract()
            
            self.progress.emit("识别完成", 100)
            self.finished.emit(True, f"最终结果：\n{client_result}\n{abstract_result}")
        except Exception as e:
            self.finished.emit(False, f"运行异常：{str(e)}")
        finally:
            self.is_running = False

    def stop(self):
        """停止任务"""
        self.is_running = False
        self.progress.emit("任务已停止", 0)
        self.finished.emit(False, "任务停止")

if __name__ == "__main__":
    TEST_AUDIO_PATH = "D:\\QQ\\2025年06月六级听力音频第2套.mp3"  # 16kHz单声道WAV格式（TeleSpeechASR要求）
    TEST_MODEL = "TeleAI/TeleSpeechASR"
    asr1 = asr(audio_path=TEST_AUDIO_PATH, model=TEST_MODEL)
    asr1_thread = QThread()
    print(asr1.text_abstract())