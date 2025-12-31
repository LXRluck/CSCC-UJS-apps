# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////

from gui.uis.windows.main_window.functions_main_window import *

import tempfile
import os

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

# IMPORT MPV PLAYER CORE
# ///////////////////////////////////////////////////////////////
from gui.core.player_core import MPVPlayerCore

# IMPORT SUBTITLEWORKER CORE
# ///////////////////////////////////////////////////////////////
from gui.core.subtitle_core import SubtitleWorker,clean_temp

# TEMP

class SetupPageVideoPlayer(QObject):
    def __init__(self):
        super().__init__()
        # PLAYER SETTINGS
        # ///////////////////////////////////////////////////////////////
        self.ui=None
        self.player_core=None
        self.is_dragging_progress=False
        self.video_select_label = None  # 视频选择提示标签
        self.video_file_path=None
        # SUBTITLE SETTINGS
        # ///////////////////////////////////////////////////////////////
        self.subtitle_worker = None  # 字幕生成线程
        self.subtitle_thread = None  # 线程容器
        self.temp_srt = None         # 临时字幕文件路径
        self.generate_subtitle_file = True  # 是否保存字幕文件
        self.subtitle_on=True #是否显示字幕
        self.subtitle_model = "base"  # whisper模型
        self.total_duration=0

    # SETUP PAGE_VIDEOPLAYER
    # ///////////////////////////////////////////////////////////////
    def setup_player(self):
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
        self.ui.load_pages.next_btn.set_icon(Functions.set_svg_icon("forward.svg"))
        self.ui.load_pages.next_btn.set_background_colors(self.themes["app_color"]["dark_one"],
            self.themes["app_color"]["dark_three"],
            self.themes["app_color"]["context_color"])
        self.ui.load_pages.next_btn.repaint()
        self.ui.load_pages.prev_btn.set_icon(Functions.set_svg_icon("backward.svg"))
        self.ui.load_pages.prev_btn.set_background_colors(self.themes["app_color"]["dark_one"],
            self.themes["app_color"]["dark_three"],
            self.themes["app_color"]["context_color"])
        self.ui.load_pages.prev_btn.repaint()
        self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("resume.svg"))
        self.ui.load_pages.stop_btn.set_background_colors(self.themes["app_color"]["dark_one"],
            self.themes["app_color"]["dark_three"],
            self.themes["app_color"]["context_color"])
        self.ui.load_pages.stop_btn.repaint()
        self.ui.load_pages.volume_btn.set_icon(Functions.set_svg_icon("sound_on.svg"))
        self.ui.load_pages.volume_btn.set_background_colors(self.themes["app_color"]["dark_one"],
            self.themes["app_color"]["dark_three"],
            self.themes["app_color"]["context_color"])
        self.ui.load_pages.volume_btn.repaint()

        self.ui.load_pages.progressbar.setRange(0,1000)
        self.ui.load_pages.progressbar.setValue(0)

        self.player_core=MPVPlayerCore()
        self.player_core.bind_to_window(self.ui.load_pages.video_widget.winId())
        self.ui.load_pages.video_widget.setToolTip("点击选择视频/音频文件播放")
        
        # 创建视频选择提示标签
        self.video_select_label = QLabel(self.ui.load_pages.video_widget)
        self.video_select_label.setObjectName("video_select_label")
        self.video_select_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 18px;
                background-color: rgba(60, 60, 60, 0.9);
                border-radius: 12px;
                padding: 30px;
                border: 2px dashed rgba(255, 255, 255, 0.3);
            }
        """)
        self.video_select_label.setText("🎬\n\n点击选择视频/音频文件播放\n\n支持格式: MP4, AVI, MKV, MOV, FLV, WMV, MP3, WAV, FLAC, AAC")
        self.video_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_select_label.setWordWrap(True)
        
        # 将标签添加到video_widget的布局中
        if self.ui.load_pages.video_widget.layout():
            self.ui.load_pages.video_widget.layout().addWidget(self.video_select_label)
        
        # self.player_core.set_progress_callback(self.progress_callback)

        self.volume_slider = PySlider(
            margin=8,
            bg_size=10,
            bg_radius=5,
            handle_margin=-3,
            handle_size=16,
            handle_radius=8,
            bg_color=self.themes["app_color"]["dark_three"],
            bg_color_hover=self.themes["app_color"]["dark_four"],
            handle_color=self.themes["app_color"]["context_color"],
            handle_color_hover=self.themes["app_color"]["context_hover"],
            handle_color_pressed=self.themes["app_color"]["context_pressed"],
        )
        self.volume_slider.setOrientation(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedHeight(120)
        
        self.volume_container = QWidget()

        self.volume_container.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.volume_container.setAttribute(Qt.WA_TranslucentBackground)

        volume_layout = QVBoxLayout(self.volume_container)
        volume_layout.setContentsMargins(10, 5, 10, 5)
        volume_layout.setAlignment(Qt.AlignCenter)
        volume_layout.addWidget(self.volume_slider)
     
        self.volume_container.setStyleSheet(f"""
            QWidget {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                padding: 5px; 
            }}
        """)
        self.volume_container.hide()     


        self.setup_subtitle_menu()
        # SET CONNECTS
        # ///////////////////////////////////////////////////////////////    
        self.ui.load_pages.video_widget.installEventFilter(self)
        self.volume_container.installEventFilter(self)
        if hasattr(self.ui, 'central_widget'):
            self.ui.central_widget.installEventFilter(self)

        # SET CONNECTS
        # ///////////////////////////////////////////////////////////////
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.ui.load_pages.volume_btn.clicked.connect(self.toggle_volume_slider)
        
        self.ui.load_pages.stop_btn.clicked.connect(self.on_toggle_play_pause)
        self.ui.load_pages.next_btn.clicked.connect(self.on_fast_forward)
        self.ui.load_pages.prev_btn.clicked.connect(self.on_fast_rewind)

        self.ui.load_pages.progressbar.sliderPressed.connect(self.on_progress_slider_pressed)
        self.ui.load_pages.progressbar.sliderReleased.connect(self.on_progress_slider_released)
        self.ui.load_pages.progressbar.valueChanged.connect(self.on_progress_slider_value_changed)

        self.player_core.set_progress_callback(self.update_progress_ui)
        self.is_dragging_progress = False


    # EVENT FILTER
    # ///////////////////////////////////////////////////////////////
    def eventFilter(self, obj, event):
        # video_widget event
        if obj == self.ui.load_pages.video_widget:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.handle_video_widget_left_click()
                    return True  
                elif event.button() == Qt.RightButton:
                    self.handle_video_widget_right_click(event.globalPos())
                    return True  
        
        # volume container
        if event.type() == QEvent.MouseButtonPress and not self.volume_container.isHidden():
            if not self.volume_container.geometry().contains(QCursor.pos()):
                self.volume_container.hide()
                return True
        
        if obj == self.volume_container and event.type() == QEvent.Resize:
            self.reposition_volume_container()
            return True
        
        return super().eventFilter(obj, event)
    

    # VOLUME FUNCTIONS
    # ///////////////////////////////////////////////////////////////
    def on_volume_changed(self, value=None):
        if value is None:
            value=self.volume_slider.value()
        self.player_core.set_volume(value)
        self.ui.load_pages.volume_btn.setToolTip(f"Volume: {value}%")

    def toggle_volume_slider(self):
        if self.volume_container.isHidden():
            btn_widget = self.ui.load_pages.volume_btn
            btn_global_pos = btn_widget.mapToGlobal(QPoint(0, 0))
            btn_width = btn_widget.width()
            btn_height = btn_widget.height()
            container_width = self.volume_container.width()
            container_height = self.volume_container.height()
            container_x = btn_global_pos.x() + (btn_width // 2) - (container_width // 2)
            container_y = btn_global_pos.y() - container_height - 5  
            if container_y < 10:
                container_y = 10
            self.volume_container.move(container_x, container_y)
            self.volume_slider.show()
            self.volume_container.show()
            current_vol = self.player_core.get_volume() or 50
            self.volume_slider.setValue(int(current_vol))
        else:
            self.volume_container.hide()

    def reposition_volume_container(self):
        if not self.volume_container.isHidden():
            btn_widget = self.ui.load_pages.volume_btn
            btn_global_pos = btn_widget.mapToGlobal(QPoint(0, 0))
            btn_width = btn_widget.width()
            btn_height = btn_widget.height()
            container_width = self.volume_container.width()
            container_height = self.volume_container.height()
            container_x = btn_global_pos.x() + (btn_width // 2) - (container_width // 2)
            container_y = btn_global_pos.y() - container_height - 5
            if container_y < 10:
                container_y = 10
            self.volume_container.move(container_x, container_y)

    
    # PROGRESSBAR FUNCTIONS
    # ///////////////////////////////////////////////////////////////
    @staticmethod
    def format_time(seconds):
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
        
    def get_current_position(self):
        return self.player_core.get_position()
    
    def update_progress_ui(self, current_pos=None, duration=None):
        if duration is None:
            duration = self.total_duration
        if self.is_dragging_progress or duration == 0:
            return
        if current_pos is None:
            current_pos = self.player_core.get_position()
        if not self.is_dragging_progress: 
            if current_pos is None:
                current_pos = self.player_core.get_position()

            progress_percent = (current_pos / duration) * 1000
            self.ui.load_pages.progressbar.setValue(int(progress_percent))

            current_time = SetupPageVideoPlayer.format_time(current_pos)
            total_time = SetupPageVideoPlayer.format_time(duration)
            self.ui.load_pages.progress_label.setText(f"{current_time}/{total_time}")

    def on_progress_slider_pressed(self):
        self.is_dragging_progress = True
        if self.player_core.is_playing:
            self.player_core.toggle_play_pause()
        

    def on_progress_slider_released(self):
        self.is_dragging_progress = False
        slider_value = self.ui.load_pages.progressbar.value()
        duration = self.total_duration
        if duration > 0:
            new_pos = (slider_value / 1000) * duration
            self.player_core.set_position(new_pos)
            self.update_progress_ui(new_pos, duration)
            if not self.player_core.is_playing and self.player_core.current_file:
                self.player_core.toggle_play_pause()

    def on_progress_slider_value_changed(self):
        if self.is_dragging_progress:
            duration = self.total_duration
            if duration > 0:
                new_pos = (self.ui.load_pages.progressbar.value() / 1000) * duration
                current_time = SetupPageVideoPlayer.format_time(new_pos)
                total_time = SetupPageVideoPlayer.format_time(duration)
                self.ui.load_pages.progress_label.setText(f"{current_time}/{total_time}")
    
    
    
    
    # PLAYER FUNCTIONS
    # ///////////////////////////////////////////////////////////////
    def handle_video_widget_left_click(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.load_pages.video_widget,
            "选择播放文件",
            os.path.expanduser("~"),
            "视频文件 (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;音频文件 (*.mp3 *.wav *.flac *.aac);;所有文件 (*.*)"
        )
        if file_path and os.path.exists(file_path):

            self.is_dragging_progress=False
            self.ui.load_pages.progressbar.setValue(0)
            self.ui.load_pages.progress_label.setText("00:00/00:00")

            self.player_core.load_video(file_path)
            self.total_duration=self.player_core.get_duration()

            file_name = os.path.basename(file_path)
            self.ui.load_pages.video_widget.setToolTip(f"当前播放：{file_name}\n点击可更换文件")
            
            self.video_file_path=file_path
            # 隐藏视频选择提示标签
            if self.video_select_label:
                self.video_select_label.hide()
                
            self.update_progress_ui(0,self.total_duration)

            #self.start_subtitle_worker(file_path)
    def handle_video_widget_right_click(self,global_pos):
        self.show_subtitle_menu(global_pos)

    def stop_playback(self):
        self.player_core.stop()
        self.ui.load_pages.video_widget.setToolTip("点击选择视频/音频文件播放")
        
        # 显示视频选择提示标签
        if self.video_select_label:
            self.video_select_label.show()

    def on_toggle_play_pause(self):
        try:
            if not hasattr(self.player_core, 'current_file') or not self.player_core.current_file:
                raise ValueError("未加载任何视频/音频文件，请先选择文件！")
            # 切换播放/暂停状态
            self.player_core.toggle_play_pause()
            # 更新按钮图标
            if self.player_core.is_playing == True:
                self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("pause.svg"))
            else:
                self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("resume.svg"))
        except AttributeError as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"播放器状态获取失败：{str(e)}")
        except ValueError as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "提示", str(e))
        except Exception as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"播放/暂停切换失败：{str(e)}")

    def on_fast_forward(self):
        try:
            if not hasattr(self.player_core, 'current_file') or not self.player_core.current_file:
                raise ValueError("未加载任何视频/音频文件，请先选择文件！")
            self.player_core.fast_forward()
            if self.player_core.is_playing == True:
                self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("resume.svg"))
            else:
                self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("pause.svg"))  
        except AttributeError as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"播放器状态获取失败：{str(e)}")
        except ValueError as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "提示", str(e))
        except Exception as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"快进失败：{str(e)}")
    
    def on_fast_rewind(self):
        try:
            if not hasattr(self.player_core, 'current_file') or not self.player_core.current_file:
                raise ValueError("未加载任何视频/音频文件，请先选择文件！")
            self.player_core.fast_rewind()
            if self.player_core.is_playing == True:
                self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("resume.svg"))
            else:
                self.ui.load_pages.stop_btn.set_icon(Functions.set_svg_icon("pause.svg"))  
        except AttributeError as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"播放器状态获取失败：{str(e)}")
        except ValueError as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "提示", str(e))
        except Exception as e:
            QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"快退失败：{str(e)}")
    
    # SUBTITLE FUNCTIONS
    # ///////////////////////////////////////////////////////////////
    def start_subtitle_worker(self, video_path):
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        if self.generate_subtitle_file:
            # 保存到视频同目录
            self.temp_srt = os.path.join(video_dir, f"{video_name}.srt")
        else:
            # 生成临时字幕文件
            temp_fd, temp_path = tempfile.mkstemp(suffix=".srt", prefix="temp_sub_")
            os.close(temp_fd)
            self.temp_srt = temp_path

        # 2. 创建字幕生成线程
        self.subtitle_worker = SubtitleWorker(
            mpv_player=self.player_core,
            video_path=video_path,
            srt_path=self.temp_srt,
            model_size=self.subtitle_model,
            total_duration=self.total_duration,
            slice_duration=10,
            short_segment_threshold=2
            
        )
        self.subtitle_thread = QThread()
        self.subtitle_worker.moveToThread(self.subtitle_thread)
        self.subtitle_worker.progress.connect(self.on_subtitle_progress)
        self.subtitle_worker.finished.connect(self.on_subtitle_finished)
        self.subtitle_thread.started.connect(self.subtitle_worker.run)
        self.subtitle_worker.subtitle_updated.connect(
            self.player_core.inject_mpv_subtitle,
            type=Qt.QueuedConnection
        )
        # 启动线程
        self.subtitle_thread.start()
        QMessageBox.information(self.ui.load_pages.video_widget, "提示", "开始生成字幕，请稍候...\n生成过程中可正常播放视频")

    def on_subtitle_progress(self, msg, progress):
        #字幕生成进度回调
        print(f"字幕生成进度：{progress}% - {msg}")  
        # self.ui.load_pages.subtitle_progress_label.setText(f"{msg} ({progress}%)")
    
    def on_subtitle_finished(self, success, msg):
        #字幕生成完成回调
        if success:
            # 加载完整的SRT字幕文件
            try:
                # 直接使用sub_file属性设置字幕文件
                self.player_core.mpv_player.sub_file = self.temp_srt
                
                # 确保字幕可见
                self.player_core.mpv_player.sub_visibility = True
                
                # 打印调试信息
                print(f"字幕文件已加载：{self.temp_srt}")
                print(f"字幕轨道ID：{self.player_core.mpv_player.sub}")
                    
            except Exception as e:
                print(f"字幕轨道设置失败：{e}")
                QMessageBox.warning(self.ui.load_pages.video_widget, "错误", f"字幕轨道设置失败：{str(e)}")
            
            QMessageBox.information(self.ui.load_pages.video_widget, "成功", msg)
        else:
            QMessageBox.warning(self.ui.load_pages.video_widget, "失败", msg)
        self.subtitle_thread.quit()
        self.subtitle_thread.wait()
        self.subtitle_worker = None
        self.subtitle_thread = None

    
    def stop_subtitle_worker(self):
        if self.subtitle_worker and self.subtitle_thread:
            self.subtitle_worker.stop()
            self.subtitle_thread.quit()
            self.subtitle_thread.wait()
            self.subtitle_worker = None
            self.subtitle_thread = None
        
        if self.temp_srt and not self.generate_subtitle_file and os.path.exists(self.temp_srt):
            clean_temp([self.temp_srt])
        self.temp_srt = None

    def set_subtitle_settings(self, generate_file: bool, model_size: str):
        self.generate_subtitle_file = generate_file
        self.subtitle_model = model_size
    
    # SUBTITLE MENU
    # ///////////////////////////////////////////////////////////////
    def setup_subtitle_menu(self):
        self.subtitle_menu=QMenu(self.ui.load_pages.video_widget)
        self.subtitle_menu.setStyleSheet("""
        QMenu {
            background-color: #1e1e1e;  
            color: #d4d4d4;             
            border: 1px solid #3c3c3c;  
            border-radius: 4px;
            padding: 4px 0;
        }
        QMenu::item {
            padding: 6px 24px;  
            margin: 0;
        }
        QMenu::item:selected {
            background-color: #0a7aca;  
            color: white;
        }
        QMenu::separator {
            height: 1px;
            background-color: #3c3c3c;
            margin: 4px 8px;
        }
        QMenu::shortcut {
            color: #8a8a8a;  
        }
        """)
    
    def show_subtitle_menu(self,pos):
        if not hasattr(self.player_core, 'current_file') or not self.player_core.current_file:
            self.subtitle_menu.clear()
            action_tip = QAction("⚠ 请先选择视频文件播放", self.subtitle_menu)
            action_tip.setDisabled(True)
            self.subtitle_menu.addAction(action_tip)
        else:
            self.subtitle_menu.clear()
            
            self.action_insert_exist_subtitle_file=QAction("选择已有字幕...",self.subtitle_menu)
            self.action_insert_exist_subtitle_file.triggered.connect(self.on_load_exist_subtitle)
            
            self.action_toggle_open_subtitle=QAction("关闭字幕...",self.subtitle_menu)
            self.action_toggle_open_subtitle.triggered.connect(self.on_toggle_open_subtitle)

            self.action_generate_subtitle=QAction("自动生成字幕...",self.subtitle_menu)
            self.action_generate_subtitle.triggered.connect(self.on_generate_subtitle)
            
            if self.subtitle_on is True :
                self.action_toggle_open_subtitle.setText("关闭字幕")
            else:    
                self.action_toggle_open_subtitle.setText("显示字幕")

            self.subtitle_menu.addAction(self.action_insert_exist_subtitle_file)
            self.subtitle_menu.addAction(self.action_toggle_open_subtitle)
            self.subtitle_menu.addAction(self.action_generate_subtitle)
    
        #在鼠标右键点击位置显示菜单
        self.subtitle_menu.exec(pos)


    def on_load_exist_subtitle(self):
        #print("on_load_exist_subtitle")
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.load_pages.video_widget,
            "选择字幕文件",
            os.path.expanduser("~"),
            "字幕文件 (*.srt);;所有文件 (*.*)"
        )
        if file_path and os.path.exists(file_path):
            self.player_core.set_subtitle_file(file_path)
    def on_toggle_open_subtitle(self):
        if self.subtitle_on is True:
            if self.player_core and self.player_core.mpv_player:
                self.subtitle_on=False
                self.player_core.mpv_player.sub_visibility = False
            #print("self.subtitle_on=False")
        else:
            
            if self.player_core and self.player_core.mpv_player:
                self.subtitle_on=True
                self.player_core.mpv_player.sub_visibility = True
            #print("self.subtitle_on=False")
    def on_generate_subtitle(self):
        self.start_subtitle_worker(self.video_file_path)









    # KEYWORD FUNCTIONS
    # ///////////////////////////////////////////////////////////////
    # 关键字提取线程
    # def start_keyword_worker(self):
        
    #     self.keyword_worker = keyword_abstract(
    #         srt_path=self.temp_srt,
    #     )
    #     self.keyword_thread = QThread()
    #     self.keyword_worker.moveToThread(self.subtitle_thread)

    #    
    #     self.keyword_worker.progress.connect(self.on_keyword_progress)
    #     self.keyword_worker.finished.connect(self.on_keyword_finished)
    #     self.keyword_thread.started.connect(self.keyword_worker.run)

    # 
    #     self.keyword_thread.start()
    #     QMessageBox.information(self.ui.load_pages.video_widget,"开始提取关键词，请稍候...")

    # def on_keyword_progress(self, msg, progress):
    #     print(f"关键字提取进度：{progress}% - {msg}")  
    # def on_keyword_finished(self, success, msg):
    #     if success:
    #         self.player_core.set_subtitle_file(self.temp_srt)
    #         QMessageBox.information(self.ui.load_pages.video_widget, "成功", msg)
    #     else:
    #         QMessageBox.warning(self.ui.load_pages.video_widget, "失败", msg)
    #     for index,key in self.keyword_worker.keywords:
    #         print(f"关键字 {index+1}:{key}")
        
    #     self.keyword_thread.quit()
    #     self.keyword_thread.wait()
    #     self.keyword_worker = None
    #     self.keyword_thread = None

    
    # def stop_keyword_worker(self):
    #     if self.keyword_worker and self.keyword_thread:
    #         self.keyword_worker.stop()
    #         self.keyword_thread.quit()
    #         self.keyword_thread.wait()
    #         self.keyword_worker = None
    #         self.keyword_thread = None
        
    #     if self.temp_srt and not self.generate_subtitle_file and os.path.exists(self.temp_srt):
    #         clean_temp([self.temp_srt])
    #     self.temp_srt = None

    # def set_keyword_settings(self, generate_file: bool, model_size: str):
    #     self.generate_subtitle_file = generate_file
    #     self.subtitle_model = model_size
    

