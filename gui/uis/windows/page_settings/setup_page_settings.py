# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.ui_main import *

# MAIN FUNCTIONS
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *

# IMPORT API UTILS
# ///////////////////////////////////////////////////////////////
from gui.core.api_utils import ASRClient


class SetupPageSettings(QObject):
    # 定义信号，用于传递API配置
    api_config_changed = Signal(str, str, str)  # (api_endpoint, api_key, model_name)
    
    def __init__(self):
        super().__init__()
        # 初始化ASR客户端
        self.asr_client = ASRClient()
        self.current_api_endpoint = ""
        self.current_api_key = ""
        self.current_model_name = ""
        self.current_file_path=r"D:\video\small_test.mp3"

    # SETUP PAGE_VIDEOPLAYER
    # ///////////////////////////////////////////////////////////////
    def setup_page_settings(self):
        # CHECK LOAD UI
        # ///////////////////////////////////////////////////////////////
        if self.ui is None:
            self.ui = UI_MainWindow()
            self.ui.setup_ui(self)
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items
        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items
        # SET THEME 
        # ///////////////////////////////////////////////////////////////
        # API SETTINGS STYLES
        self.ui.load_pages.line_api_endpoint.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.line_api_key.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.line_model_name.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.toggle_local_remote.set_stylesheet(
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["icon_color"],
            active_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.btn_check.set_style(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.ui.load_pages.btn_apply.set_style(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        # THEMES SETTINGS STYLES
        self.ui.load_pages.comboBox_themes.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        # SUBTITLE SETTINGS STYLES
        self.ui.load_pages.comboBox_sub_model.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.toggle_save_subtitles.set_stylesheet(
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["icon_color"],
            active_color = self.themes["app_color"]["context_color"]
        )

        # 连接API配置输入框的信号
        self.connect_api_config_signals()

        self.ui.load_pages.btn_check.clicked.connect(self.on_check_status)
        self.ui.load_pages.btn_apply.clicked.connect(self.apply_api_settings)

    def connect_api_config_signals(self):
        """
        连接API配置输入框的信号，实时监听配置变化
        """
         # 连接line_api_endpoint (ASR API ENDPOINT)
        if hasattr(self.ui.load_pages, 'line_api_endpoint'):
            self.ui.load_pages.line_api_endpoint.textChanged.connect(self.on_api_endpoint_changed)
    
        # 连接line_api_key (API KEY)
        if hasattr(self.ui.load_pages, 'line_api_key'):
            self.ui.load_pages.line_api_key.textChanged.connect(self.on_api_key_changed)
    
        # 连接line_model_name (MODEL NAME)
        if hasattr(self.ui.load_pages, 'line_model_name'):
            self.ui.load_pages.line_model_name.textChanged.connect(self.on_model_name_changed)
    
    def on_api_endpoint_changed(self, text):
        """
        API端点URL变化时的处理
        """
        self.current_api_endpoint = text
        self.update_api_config()
    
    def on_api_key_changed(self, text):
        """
        API密钥变化时的处理
        """
        self.current_api_key = text
        self.update_api_config()
    
    def on_model_name_changed(self, text):
        """
        模型名称变化时的处理
        """
        self.current_model_name = text
        self.update_api_config()
    
    def update_api_config(self):
        """
        更新API配置并发出信号
        """
        # 更新ASR客户端的凭证
        if self.current_api_endpoint and self.current_api_key:
            self.asr_client.set_credentials(
                api_endpoint=self.current_api_endpoint,
                api_key=self.current_api_key
            )
        
        # 发出信号，通知其他组件配置已更新
        self.api_config_changed.emit(
            self.current_api_endpoint,
            self.current_api_key,
            self.current_model_name
        )
    def get_api_config(self):
        """
        获取当前的API配置
        
        Returns:
            tuple: (api_endpoint, api_key, model_name)
        """
        return (
            self.current_api_endpoint,
            self.current_api_key,
            self.current_model_name
        )
    def get_asr_client(self):
        """
        获取ASR客户端实例
        
        Returns:
            ASRClient: ASR客户端对象
        """
        return self.asr_client
    
    def test_asr_connection(self,audio_path):
        """
        测试ASR连接和API调用（示例方法）
        
        Args:
            audio_file_path: 音频文件路径
        
        Returns:
            str: 识别的文本内容，失败时返回错误信息
        """
        try:
            # 检查配置是否完整
            if not self.current_api_endpoint:
                return "错误：API端点未设置"
            if not self.current_api_key:
                return "错误：API密钥未设置"
            if not self.current_model_name:
                return "错误：模型名称未设置"
            
            # 调用ASR客户端进行语音识别
            result = self.asr_client.transcribe(
                file_path=audio_path,
                model=self.current_model_name
            )
            
            if result:
                return f"识别成功：{result}"
            else:
                return "识别失败：未返回结果"
        
        except ValueError as e:
            return f"参数错误：{str(e)}"
        except FileNotFoundError as e:
            return f"文件错误：{str(e)}"
        except Exception as e:
            return f"请求失败：{str(e)}"
        
    def on_check_status(self):
        res=self.test_asr_connection(self.current_file_path)
        if res.startswith("识别成功"): 
            self.ui.load_pages.label_status.setText("CONNECTED")
            self.ui.load_pages.label_status.setStyleSheet("color: #00FF00;") 
        else:
            self.ui.load_pages.label_status.setText("ERROR")
            self.ui.load_pages.label_status.setStyleSheet("color: #FF0000;")

    def apply_api_settings(self):
        self.current_api_endpoint=self.ui.load_pages.line_api_endpoint.text()
        self.current_api_key=self.ui.load_pages.line_api_key.text()
        self.current_model_name=self.ui.load_pages.line_model_name.text()
        #self.current_file_path=self.ui.load_pages.line_file.text()
        self.update_api_config()


        