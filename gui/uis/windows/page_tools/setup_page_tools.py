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

# MAIN FUNCTIONS
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.page_videoplayer.setup_page_videoplayer import SetupPageVideoPlayer

# IMPORT KEYWORD AND SUMMARY MODULES
# ///////////////////////////////////////////////////////////////
from gui.core.keyword_core import KeywordAbstract
from gui.core.summary_core import Summary

import os

class SetupPageTools(QObject):
    def __init__(self):
        super().__init__()
        self.video_class=None
        self.ui=None

        self.keyword_num=1
        self.keysentence_num=1
    # SETUP PAGE_TOOLS
    # ///////////////////////////////////////////////////////////////
    def setup_page_tools(self):
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
        self.ui.load_pages.line_file.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.toggle_edit.set_stylesheet(
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["icon_color"],
            active_color = self.themes["app_color"]["context_color"]
        )
        self.ui.load_pages.toggle_edit.setEnabled(False)
        self.ui.load_pages.btn_file.set_style(
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
            value = 0,
            progress_color = self.themes["app_color"]["context_color"],
            text_color = self.themes["app_color"]["text_title"],
            font_size = 14,
            bg_color = self.themes["app_color"]["dark_four"]
        )
        self.circular_progress_sub.setFixedSize(200,200)
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
        self.table_sub.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  
        self.table_sub.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_sub.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_sub.verticalHeader().setVisible(False)
        self.table_sub.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Columns / Header
        header = self.table_sub.horizontalHeader()
        for idx in range(3):
            if idx == 2:  
                header.setSectionResizeMode(idx, QHeaderView.Stretch)
            else:  
                header.setSectionResizeMode(idx, QHeaderView.Fixed)

        QTimer.singleShot(0, self.set_table_column_widths)

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

        #test
        # for x in range(10):
        #     row_number = self.table_sub.rowCount()
        #     self.table_sub.insertRow(row_number) # Insert row
        #     self.table_sub.setItem(row_number, 0, QTableWidgetItem(str("Wanderson"))) # Add name
        #     self.table_sub.setItem(row_number, 1, QTableWidgetItem(str("vfx_on_fire_" + str(x)))) # Add nick
        #     self.pass_text = QTableWidgetItem()
        #     self.pass_text.setTextAlignment(Qt.AlignCenter)
        #     self.pass_text.setText("12345" + str(x))
        #     self.table_sub.setItem(row_number, 2, self.pass_text) # Add pass
        #     self.table_sub.setRowHeight(row_number, 40)

        self.ui.load_pages.layout_subtitle_table.addWidget(self.table_sub)

        self.ui.load_pages.btn_keyword.set_style(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )

        self.ui.load_pages.btn_summary.set_style(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )

        self.ui.load_pages.comboBox_keynum.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]

        )



        self.ui.load_pages.comboBox_topK.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]

        )

        self.ui.load_pages.plainTextEdit.set_stylesheet(
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        # SET CONNECTIONS
        # ///////////////////////////////////////////////////////////////
        self.ui.load_pages.btn_file.clicked.connect(self.open_file)
        self.ui.load_pages.btn_save_sub.clicked.connect(self.save_subtitle)
        #self.ui.load_pages.btn_start_sub.clicked.connect(self.video_class.start_subtitle_process)
        self.ui.load_pages.btn_keyword.clicked.connect(self.start_keyword_worker)
        self.ui.load_pages.btn_summary.clicked.connect(self.start_summary_worker)

        self.ui.load_pages.comboBox_keynum.currentIndexChanged.connect(self.update_btn_keyword)
        self.ui.load_pages.comboBox_topK.currentIndexChanged.connect(self.set_keysentence_num)
# BIND CONNECTIONS
# ///////////////////////////////////////////////////////////////
    def bind_video_class(self,video_settings:SetupPageVideoPlayer):
        self.video_class=video_settings
        self.video_class.subtitle_progress_updated.connect(self.update_circular_progress)
        
        self.video_class.video_path_updated.connect(self.ui.load_pages.line_file.setText)

        self.total_subtext=""
        self.video_class.subtitle_sentence_updated.connect(self.update_subtitle_table)
        
        self.sub_status=0
        self.video_class.sub_generate_status_changed.connect(self.update_sub_generate_status)

    def update_circular_progress(self,progress):
        self.circular_progress_sub.set_value(progress)

    def update_subtitle_table(self,index,start,end,text):
        self.total_subtext=self.total_subtext+text
        row_number = self.table_sub.rowCount()
        self.table_sub.insertRow(row_number)
        self.table_sub.setItem(row_number, 0, QTableWidgetItem(str(index))) # Add index
        time_text = f"{self.video_class.format_time(start)} --> {self.video_class.format_time(end)}"
        self.table_sub.setItem(row_number, 1, QTableWidgetItem(time_text)) # Add time
        self.table_sub.setItem(row_number, 2, QTableWidgetItem(text)) # Add content
        self.table_sub.setRowHeight(row_number, 40)
        self.ui.load_pages.layout_subtitle_table.addWidget(self.table_sub)
    
    def update_sub_generate_status(self,status):
        self.sub_status=status
        if status==0:
            self.ui.load_pages.toggle_edit.setEnabled(False)
            self.ui.load_pages.btn_keyword.setEnabled(False)
            self.ui.load_pages.btn_summary.setEnabled(False)
            self.ui.load_pages.btn_save_sub.setEnabled(False)
            self.ui.load_pages.btn_start_sub.setEnabled(False)
            self.table_sub.setEditTriggers(QAbstractItemView.NoEditTriggers)
        elif status==1:
            pass
        elif status==2:
            self.ui.load_pages.toggle_edit.setEnabled(True)
            self.ui.load_pages.btn_keyword.setEnabled(True)
            self.ui.load_pages.btn_summary.setEnabled(True)
            self.ui.load_pages.btn_save_sub.setEnabled(True)
            self.ui.load_pages.btn_start_sub.setEnabled(True)
            self.table_sub.setEditTriggers(QAbstractItemView.AllEditTriggers)
            print(self.total_subtext)

    def update_btn_keyword(self):
        num_key=int(self.ui.load_pages.comboBox_keynum.currentText())
        self.keyword_num=num_key
        self.setup_push_buttons_status(num_key)

    def set_keysentence_num(self):
        self.keysentence_num=int(self.ui.load_pages.comboBox_topK.currentText())

    def setup_push_buttons_status(self,num):
        for btn_num in range(1, num+1):
            btn_attr_name = f"pushButton_{btn_num}"
            if hasattr(self.ui.load_pages, btn_attr_name):
                btn = getattr(self.ui.load_pages, btn_attr_name)
                btn.show()
            else:
                print(f"Warning: Button {btn_attr_name} not found in load_pages!")
        for btn_num in range(num+1, 11):
            btn_attr_name = f"pushButton_{btn_num}"
            if hasattr(self.ui.load_pages, btn_attr_name):
                btn = getattr(self.ui.load_pages, btn_attr_name)
                btn.hide()
            else:
                print(f"Warning: Button {btn_attr_name} not found in load_pages!")


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
                btn.setText("KEYWORD")
                btn.hide()
            else:
                print(f"Warning: Button {btn_attr_name} not found in load_pages!")
        self.ui.load_pages.pushButton_1.show()  
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.load_pages.video_widget,
            "选择播放文件",
            os.path.expanduser("~"),
            "视频文件 (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;音频文件 (*.mp3 *.wav *.flac *.aac);;所有文件 (*.*)"
        )
        if file_path and os.path.exists(file_path):
            
            self.ui.load_pages.line_file.setText(file_path)
            
    def save_subtitle(self):
        pass


    def set_table_column_widths(self):
            weights = [1, 3, 6]
            total_weight = sum(weights[:2])  
            table_width = self.table_sub.viewport().width() 
            
            col0_width = int(table_width * (weights[0] / (total_weight + weights[2])))
            col1_width = int(table_width * (weights[1] / (total_weight + weights[2])))
            
            self.table_sub.setColumnWidth(0, col0_width)
            self.table_sub.setColumnWidth(1, col1_width)


    

    
# KEYWORD FUNCTIONS
# ///////////////////////////////////////////////////////////////
    # 关键字提取线程
    def start_keyword_worker(self):
        # if not self.temp_srt or not os.path.exists(self.temp_srt):
        #     QMessageBox.warning(
        #         self.ui.load_pages.video_widget,
        #         "参数错误",
        #         "字幕文件不存在，无法提取关键字！\n请先生成或加载字幕。"
        #     )
        #     return
        self.keyword_worker = KeywordAbstract(subtext=self.total_subtext,srt_path=None,topK=self.keyword_num)
        self.keyword_thread = QThread(parent=self)  # 设置父对象，避免内存泄漏
        self.keyword_worker.moveToThread(self.keyword_thread)

        self.keyword_worker.progress.connect(self.on_keyword_progress)
        self.keyword_worker.finished.connect(self.on_keyword_finished)
        self.keyword_thread.started.connect(self.keyword_worker.run)
        self.keyword_thread.finished.connect(self.keyword_thread.deleteLater)

        self.keyword_thread.start()

    def on_keyword_progress(self, msg, progress):
        print(f"关键字提取进度：{progress}% - {msg}")  

    def on_keyword_finished(self, success, msg):
        if success:
            QMessageBox.information(self.ui.load_pages.video_widget, "成功", msg)
            self.show_keywords()
        else:
            QMessageBox.warning(self.ui.load_pages.video_widget, "失败", msg)

        if self.keyword_thread and self.keyword_thread.isRunning():
            self.keyword_thread.quit()
            self.keyword_thread.wait()  
        self.keyword_worker = None
        self.keyword_thread = None
        

    def stop_keyword_worker(self):
        if self.keyword_worker and self.keyword_thread and self.keyword_thread.isRunning():
            self.keyword_worker.stop()
            self.keyword_thread.quit()
            self.keyword_thread.wait()
            self.keyword_worker = None
            self.keyword_thread = None

    def set_keyword_settings(self, keyword_topK: int = 4):
   
        self.keyword_topK = keyword_topK  


    def show_keywords(self):
        print(f"关键字提取结果：{self.keyword_worker.keywords}")
        for index, key in enumerate(self.keyword_worker.keywords):
            btn_attr_name = f"pushButton_{index+1}"
            if hasattr(self.ui.load_pages, btn_attr_name):
                btn = getattr(self.ui.load_pages, btn_attr_name)
                btn.setText(f"{key}")
                btn.show()
            else:
                print(f"Warning: Button {btn_attr_name} not found in load_pages!")


# SUMMARY FUNCTIONS
# ///////////////////////////////////////////////////////////////
    # 摘要提取线程
    def start_summary_worker(self):
        self.summary_worker = Summary(sub_text=self.total_subtext,topK=self.keysentence_num)
        self.summary_thread = QThread(parent=self)  
        self.summary_worker.moveToThread(self.summary_thread)

        self.summary_worker.progress.connect(self.on_summary_progress)
        self.summary_worker.finished.connect(self.on_summary_finished)
        self.summary_thread.started.connect(self.summary_worker.run)
        self.summary_thread.finished.connect(self.summary_thread.deleteLater)

        self.summary_thread.start()
        QMessageBox.information(
            self.ui.load_pages.video_widget,
            "关键词提取",
            "关键词提取已启动，可在后台运行\n进度将在控制台打印"
        )

    def on_summary_progress(self, msg, progress):
        print(f"摘要进度：{progress}% - {msg}")  

    def on_summary_finished(self, success, msg):
        if success:
            QMessageBox.information(self.ui.load_pages.video_widget, "成功", msg)
            self.on_summary_result(self.summary_worker.key_sentences)
        else:
            QMessageBox.warning(self.ui.load_pages.video_widget, "失败", msg)

        # 停止线程
        if self.summary_thread and self.summary_thread.isRunning():
            self.summary_thread.quit()
            self.summary_thread.wait()  
        self.summary_worker = None
        self.summary_thread = None
    def on_summary_result(self, sentences):

        self.ui.load_pages.plainTextEdit.clear()  
    
        # 整理摘要内容
        summary_text = ""

        for idx, item in enumerate(sentences, 1):
            summary_text += f"{idx}. {item['sentence']}\n\n"
    
        self.ui.load_pages.plainTextEdit.setPlainText(summary_text)

    def stop_summary_worker(self):
        if self.summary_worker and self.summary_thread and self.summary_thread.isRunning():
            self.summary_worker.stop()
            self.summary_thread.quit()
            self.summary_thread.wait()
            self.summary_worker = None
            self.summary_thread = None


        