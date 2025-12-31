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


class SetupPageTools(QObject):
    # 定义信号，用于传递API配置
    api_config_changed = Signal(str, str, str)  # (api_endpoint, api_key, model_name)
    
    def __init__(self):
        super().__init__()
        # 初始化ASR客户端
        self.asr_client = ASRClient()
        self.current_api_endpoint = ""
        self.current_api_key = ""
        self.current_model_name = ""

    # SETUP PAGE_VIDEOPLAYER
    # ///////////////////////////////////////////////////////////////
    def setup_tools(self):
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
        self.setup_push_buttons_style()
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


        self.ui.load_pages.checkBox.set_stylesheet(
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

        self.ui.load_pages.btn_save_sub.set_style(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )

        self.ui.load_pages.btn_start_sub.set_style(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )

        self.circular_progress_sub = PyCircularProgress(
            value = 75,
            progress_width = 2,
            progress_color = self.themes["app_color"]["pink"],
            text_color = self.themes["app_color"]["white"],
            font_size = 14,
            bg_color = self.themes["app_color"]["bg_three"]
        )
        self.circular_progress_sub.setFixedSize(140,140)
        self.ui.load_pages.layout_circular_bar.addWidget(self.circular_progress_sub)


        self.table_sub = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.table_sub.setColumnCount(3)
        self.table_sub.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_sub.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_sub.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Columns / Header
        self.column_index = QTableWidgetItem()
        self.column_index.setTextAlignment(Qt.AlignCenter)
        self.column_index.setText("INDEX")

        self.column_time = QTableWidgetItem()
        self.column_time.setTextAlignment(Qt.AlignCenter)
        self.column_time.setText("TIME")

        self.column_content = QTableWidgetItem()
        self.column_content.setTextAlignment(Qt.AlignCenter)
        self.column_content.setText("CONTENT")

        # Set column
        self.table_sub.setHorizontalHeaderItem(0, self.column_index)
        self.table_sub.setHorizontalHeaderItem(1, self.column_time)
        self.table_sub.setHorizontalHeaderItem(2, self.column_content)

        # test
        for x in range(10):
            row_number = self.table_sub.rowCount()
            self.table_sub.insertRow(row_number) # Insert row
            self.table_sub.setItem(row_number, 0, QTableWidgetItem(str("Wanderson"))) # Add name
            self.table_sub.setItem(row_number, 1, QTableWidgetItem(str("vfx_on_fire_" + str(x)))) # Add nick
            self.pass_text = QTableWidgetItem()
            self.pass_text.setTextAlignment(Qt.AlignCenter)
            self.pass_text.setText("12345" + str(x))
            self.table_sub.setItem(row_number, 2, self.pass_text) # Add pass
            self.table_sub.setRowHeight(row_number, 40)

        self.ui.load_pages.layout_subtitle_table.addWidget(self.table_sub)

        # 测试连通性按钮
        self.ui.load_pages.btn_check.clicked.connect(self.on_btn_check_clicked)

        # 开始识别按钮
        self.ui.load_pages.btn_start_sub.clicked.connect(self.on_btn_start_sub_clicked)

        # 保存配制按钮
        self.ui.load_pages.btn_save_sub.clicked.connect(self.on_btn_save_sub_clicked)


        # self.ui.load_pages.comboBox.set_stylesheet(
        #     radius = 8,
        #     border_size = 2,
        #     color = self.themes["app_color"]["text_foreground"],
        #     selection_color = self.themes["app_color"]["white"],
        #     bg_color = self.themes["app_color"]["dark_one"],
        #     bg_color_active = self.themes["app_color"]["dark_three"],
        #     context_color = self.themes["app_color"]["context_color"]

        # )

    
        # self.ui.load_pages.plainTextEdit.set_stylesheet(
        #     radius = 8,
        #     border_size = 2,
        #     color = self.themes["app_color"]["text_foreground"],
        #     selection_color = self.themes["app_color"]["white"],
        #     bg_color = self.themes["app_color"]["dark_one"],
        #     bg_color_active = self.themes["app_color"]["dark_three"],
        #     context_color = self.themes["app_color"]["context_color"]
        # )

    
    def on_btn_check_clicked(self):
        test_audio_path = "test_audio.mp3"
        result = self.test_asr_connection(test_audio_path)

        QMessageBox.information(None, "连通性测试结果", result)


    def setup_push_buttons_style(self):
        btn_style = {
            "radius": 10,
            "color": self.themes["app_color"]["text_foreground"],
            "bg_color": self.themes["app_color"]["dark_one"],
            "bg_color_hover": self.themes["app_color"]["dark_three"],
            "bg_color_pressed": self.themes["app_color"]["dark_four"]
        }
        for btn_num in range(1, 11):
            btn_attr_name = f"pushButton_{btn_num}"

            if hasattr(self.ui.load_pages, btn_attr_name):
                btn = getattr(self.ui.load_pages, btn_attr_name)
                btn.set_style(**btn_style)
                btn.setMinimumHeight(80)
                btn.setText("KEYWORD")
            else:
                print(f"Warning: Button {btn_attr_name} not found in load_pages!")
        
        # 连接API配置输入框的信号
        self.connect_api_config_signals()
    
    def connect_api_config_signals(self):
        """
        连接API配置输入框的信号，实时监听配置变化
        """
        # 连接lineEdit1 (ASR API ENDPOINT)
        if hasattr(self.ui.load_pages, 'lineEdit1'):
            self.ui.load_pages.line_api_endpoint.textChanged.connect(self.on_api_endpoint_changed)
        
        # 连接lineEdit2 (API KEY)
        if hasattr(self.ui.load_pages, 'lineEdit2'):
            self.ui.load_pages.line_api_key.textChanged.connect(self.on_api_key_changed)
        
        # 连接lineEdit3 (MODEL NAME)
        if hasattr(self.ui.load_pages, 'lineEdit3'):
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
    
    def test_asr_connection(self, audio_file_path):
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
                file_path=audio_file_path,
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

    

    



