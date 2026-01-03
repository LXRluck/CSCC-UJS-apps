# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

from gui.widgets.py_combobox.py_combobox import PyComboBox
from gui.widgets.py_icon_button.py_icon_button import PyIconButton
from gui.widgets.py_line_edit.py_line_edit import PyLineEdit
from gui.widgets.py_plain_text_edit.py_plain_text_edit import PyPlainTextEdit
from gui.widgets.py_push_button.py_push_button import PyPushButton
from gui.widgets.py_slider.py_slider import PySlider
from gui.widgets.py_toggle.py_toggle import PyToggle

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(895, 697)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_home)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = QFrame(self.page_home)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.Shape.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Shadow.Raised)
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.Shape.NoFrame)
        self.logo.setFrameShadow(QFrame.Shadow.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)

        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.center_page_layout.addWidget(self.label)


        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pages.addWidget(self.page_home)
        self.page_samples = QWidget()
        self.page_samples.setObjectName(u"page_samples")
        self.page_2_layout = QVBoxLayout(self.page_samples)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_samples)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 233, 265))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_samples)
        self.page_videoplayer = QWidget()
        self.page_videoplayer.setObjectName(u"page_videoplayer")
        self.page_videoplayer.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.page_videoplayer)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.video_widget = QWidget(self.page_videoplayer)
        self.video_widget.setObjectName(u"video_widget")
        self.video_widget.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"font: 500 15pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")
        self.verticalLayout_6 = QVBoxLayout(self.video_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")

        self.verticalLayout_3.addWidget(self.video_widget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.prev_btn = PyIconButton(self.page_videoplayer)
        self.prev_btn.setObjectName(u"prev_btn")
        self.prev_btn.setMinimumSize(QSize(40, 40))
        self.prev_btn.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.prev_btn)

        self.stop_btn = PyIconButton(self.page_videoplayer)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setMinimumSize(QSize(40, 40))
        self.stop_btn.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.stop_btn)

        self.next_btn = PyIconButton(self.page_videoplayer)
        self.next_btn.setObjectName(u"next_btn")
        self.next_btn.setMinimumSize(QSize(40, 40))
        self.next_btn.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.next_btn)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.horizontalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.progressbar = PySlider(self.page_videoplayer)
        self.progressbar.setObjectName(u"progressbar")
        self.progressbar.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.progressbar)

        self.progress_label = QLabel(self.page_videoplayer)
        self.progress_label.setObjectName(u"progress_label")
        self.progress_label.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.progress_label)

        self.volume_btn = PyIconButton(self.page_videoplayer)
        self.volume_btn.setObjectName(u"volume_btn")
        self.volume_btn.setMinimumSize(QSize(40, 40))

        self.horizontalLayout_2.addWidget(self.volume_btn)

        self.horizontalLayout_2.setStretch(0, 8)
        self.horizontalLayout_2.setStretch(2, 1)

        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalLayout_3.setStretch(0, 11)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.pages.addWidget(self.page_videoplayer)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.verticalLayout_19 = QVBoxLayout(self.page_settings)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.groupBox_3 = QGroupBox(self.page_settings)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"    padding-top: 10px;\n"
"    padding-left: 8px;\n"
"    padding-right: 8px;\n"
"    padding-bottom: 8px;\n"
"	font: 14pt \"JetBrains Mono\";\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.groupBox = QGroupBox(self.groupBox_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"    padding-top: 10px;\n"
"    padding-left: 8px;\n"
"    padding-right: 8px;\n"
"    padding-bottom: 8px;\n"
"	font: 14pt \"JetBrains Mono\";\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.line_api_endpoint = PyLineEdit(self.groupBox)
        self.line_api_endpoint.setObjectName(u"line_api_endpoint")
        self.line_api_endpoint.setMinimumSize(QSize(80, 30))
        font1 = QFont()
        font1.setPointSize(12)
        self.line_api_endpoint.setFont(font1)

        self.verticalLayout_2.addWidget(self.line_api_endpoint)


        self.verticalLayout_14.addLayout(self.verticalLayout_2)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.verticalLayout_15.addLayout(self.horizontalLayout_6)

        self.line_api_key = PyLineEdit(self.groupBox)
        self.line_api_key.setObjectName(u"line_api_key")
        self.line_api_key.setMinimumSize(QSize(0, 30))
        self.line_api_key.setFont(font1)

        self.verticalLayout_15.addWidget(self.line_api_key)


        self.verticalLayout_14.addLayout(self.verticalLayout_15)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_16.addLayout(self.horizontalLayout_7)

        self.line_model_name = PyLineEdit(self.groupBox)
        self.line_model_name.setObjectName(u"line_model_name")
        self.line_model_name.setMinimumSize(QSize(0, 30))
        self.line_model_name.setFont(font1)

        self.verticalLayout_16.addWidget(self.line_model_name)


        self.verticalLayout_14.addLayout(self.verticalLayout_16)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_8.addWidget(self.label_8)

        self.toggle_local_remote = PyToggle(self.groupBox)
        self.toggle_local_remote.setObjectName(u"toggle_local_remote")

        self.horizontalLayout_8.addWidget(self.toggle_local_remote)

        self.horizontalSpacer_4 = QSpacerItem(200, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_14.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.btn_apply = PyPushButton(self.groupBox)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_11.addWidget(self.btn_apply)

        self.btn_check = PyPushButton(self.groupBox)
        self.btn_check.setObjectName(u"btn_check")
        self.btn_check.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_11.addWidget(self.btn_check)

        self.label_status = QLabel(self.groupBox)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_11.addWidget(self.label_status)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)


        self.verticalLayout_14.addLayout(self.horizontalLayout_11)


        self.verticalLayout_9.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.groupBox_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"    padding-top: 10px;\n"
"    padding-left: 8px;\n"
"    padding-right: 8px;\n"
"    padding-bottom: 8px;\n"
"	font: 14pt \"JetBrains Mono\";\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(250, 30))
        self.label_12.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_16.addWidget(self.label_12)

        self.comboBox_sub_model = PyComboBox(self.groupBox_2)
        self.comboBox_sub_model.addItem("")
        self.comboBox_sub_model.addItem("")
        self.comboBox_sub_model.addItem("")
        self.comboBox_sub_model.setObjectName(u"comboBox_sub_model")
        self.comboBox_sub_model.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setPointSize(14)
        self.comboBox_sub_model.setFont(font2)

        self.horizontalLayout_16.addWidget(self.comboBox_sub_model)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_7)


        self.verticalLayout_17.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(250, 30))
        self.label_13.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_17.addWidget(self.label_13)

        self.toggle_save_subtitles = PyToggle(self.groupBox_2)
        self.toggle_save_subtitles.setObjectName(u"toggle_save_subtitles")

        self.horizontalLayout_17.addWidget(self.toggle_save_subtitles)

        self.horizontalSpacer_8 = QSpacerItem(200, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_8)


        self.verticalLayout_17.addLayout(self.horizontalLayout_17)


        self.verticalLayout_9.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"    padding-top: 10px;\n"
"    padding-left: 8px;\n"
"    padding-right: 8px;\n"
"    padding-bottom: 8px;\n"
"	font: 14pt \"JetBrains Mono\";\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(250, 30))
        self.label_14.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_18.addWidget(self.label_14)

        self.comboBox_themes = PyComboBox(self.groupBox_4)
        self.comboBox_themes.addItem("")
        self.comboBox_themes.addItem("")
        self.comboBox_themes.setObjectName(u"comboBox_themes")
        self.comboBox_themes.setMinimumSize(QSize(0, 30))
        self.comboBox_themes.setFont(font2)

        self.horizontalLayout_18.addWidget(self.comboBox_themes)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_9)


        self.verticalLayout_18.addLayout(self.horizontalLayout_18)


        self.verticalLayout_9.addWidget(self.groupBox_4)


        self.verticalLayout_19.addWidget(self.groupBox_3)

        self.pages.addWidget(self.page_settings)
        self.page_tools = QWidget()
        self.page_tools.setObjectName(u"page_tools")
        self.verticalLayout_13 = QVBoxLayout(self.page_tools)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_7 = QLabel(self.page_tools)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_15.addWidget(self.label_7)

        self.line_file = PyLineEdit(self.page_tools)
        self.line_file.setObjectName(u"line_file")
        self.line_file.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_15.addWidget(self.line_file)

        self.btn_file = PyPushButton(self.page_tools)
        self.btn_file.setObjectName(u"btn_file")
        self.btn_file.setMinimumSize(QSize(150, 30))
        self.btn_file.setFont(font1)

        self.horizontalLayout_15.addWidget(self.btn_file)

        self.horizontalLayout_15.setStretch(1, 6)

        self.verticalLayout_7.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.btn_start_sub = PyPushButton(self.page_tools)
        self.btn_start_sub.setObjectName(u"btn_start_sub")
        self.btn_start_sub.setMinimumSize(QSize(0, 30))

        self.verticalLayout_8.addWidget(self.btn_start_sub)

        self.btn_save_sub = PyPushButton(self.page_tools)
        self.btn_save_sub.setObjectName(u"btn_save_sub")
        self.btn_save_sub.setMinimumSize(QSize(0, 30))

        self.verticalLayout_8.addWidget(self.btn_save_sub)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(self.page_tools)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_10.addWidget(self.label_6)

        self.toggle_edit = PyToggle(self.page_tools)
        self.toggle_edit.setObjectName(u"toggle_edit")

        self.horizontalLayout_10.addWidget(self.toggle_edit)


        self.verticalLayout_8.addLayout(self.horizontalLayout_10)

        self.layout_circular_bar = QVBoxLayout()
        self.layout_circular_bar.setObjectName(u"layout_circular_bar")

        self.verticalLayout_8.addLayout(self.layout_circular_bar)

        self.verticalLayout_8.setStretch(2, 1)
        self.verticalLayout_8.setStretch(3, 3)

        self.horizontalLayout_9.addLayout(self.verticalLayout_8)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_3 = QLabel(self.page_tools)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_11.addWidget(self.label_3)

        self.layout_subtitle_table = QVBoxLayout()
        self.layout_subtitle_table.setObjectName(u"layout_subtitle_table")

        self.verticalLayout_11.addLayout(self.layout_subtitle_table)

        self.verticalLayout_11.setStretch(1, 4)

        self.horizontalLayout_9.addLayout(self.verticalLayout_11)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 4)

        self.verticalLayout_7.addLayout(self.horizontalLayout_9)


        self.verticalLayout_5.addLayout(self.verticalLayout_7)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_9 = QLabel(self.page_tools)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_12.addWidget(self.label_9)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_15 = QLabel(self.page_tools)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_20.addWidget(self.label_15)

        self.comboBox_keynum = PyComboBox(self.page_tools)
        self.comboBox_keynum.addItem("")
        self.comboBox_keynum.addItem("")
        self.comboBox_keynum.addItem("")
        self.comboBox_keynum.addItem("")
        self.comboBox_keynum.setObjectName(u"comboBox_keynum")
        self.comboBox_keynum.setMinimumSize(QSize(150, 30))
        self.comboBox_keynum.setFont(font1)

        self.horizontalLayout_20.addWidget(self.comboBox_keynum)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_20)

        self.btn_keyword = PyPushButton(self.page_tools)
        self.btn_keyword.setObjectName(u"btn_keyword")
        self.btn_keyword.setMinimumSize(QSize(150, 30))
        self.btn_keyword.setFont(font1)

        self.horizontalLayout_12.addWidget(self.btn_keyword)


        self.verticalLayout_10.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_3 = PyPushButton(self.page_tools)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(100, 40))
        self.pushButton_3.setMaximumSize(QSize(100, 40))
        self.pushButton_3.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)

        self.pushButton_7 = PyPushButton(self.page_tools)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(100, 40))
        self.pushButton_7.setMaximumSize(QSize(100, 40))
        self.pushButton_7.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_7, 1, 2, 1, 1)

        self.pushButton_8 = PyPushButton(self.page_tools)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setMinimumSize(QSize(100, 40))
        self.pushButton_8.setMaximumSize(QSize(100, 40))
        self.pushButton_8.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_8, 1, 3, 1, 1)

        self.pushButton_4 = PyPushButton(self.page_tools)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(100, 40))
        self.pushButton_4.setMaximumSize(QSize(100, 40))
        self.pushButton_4.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_4, 0, 3, 1, 1)

        self.pushButton_10 = PyPushButton(self.page_tools)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setMinimumSize(QSize(100, 40))
        self.pushButton_10.setMaximumSize(QSize(100, 40))
        self.pushButton_10.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_10, 1, 4, 1, 1)

        self.pushButton_2 = PyPushButton(self.page_tools)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(100, 40))
        self.pushButton_2.setMaximumSize(QSize(100, 40))
        self.pushButton_2.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)

        self.pushButton_9 = PyPushButton(self.page_tools)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setMinimumSize(QSize(100, 40))
        self.pushButton_9.setMaximumSize(QSize(100, 40))
        self.pushButton_9.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_9, 1, 0, 1, 1)

        self.pushButton_5 = PyPushButton(self.page_tools)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(100, 40))
        self.pushButton_5.setMaximumSize(QSize(100, 40))
        self.pushButton_5.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_5, 0, 4, 1, 1)

        self.pushButton_1 = PyPushButton(self.page_tools)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.pushButton_1.setMinimumSize(QSize(100, 40))
        self.pushButton_1.setMaximumSize(QSize(100, 40))
        self.pushButton_1.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_1, 0, 0, 1, 1)

        self.pushButton_6 = PyPushButton(self.page_tools)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(100, 40))
        self.pushButton_6.setMaximumSize(QSize(100, 40))
        self.pushButton_6.setStyleSheet(u"font: 14pt \"JetBrains Mono\";")

        self.gridLayout.addWidget(self.pushButton_6, 1, 1, 1, 1)


        self.horizontalLayout_13.addLayout(self.gridLayout)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_10)

        self.horizontalLayout_13.setStretch(0, 1)
        self.horizontalLayout_13.setStretch(1, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_13)


        self.verticalLayout_5.addLayout(self.verticalLayout_10)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_10 = QLabel(self.page_tools)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_14.addWidget(self.label_10)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_11)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_11 = QLabel(self.page_tools)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font: 14pt \"JetBrains Mono\";\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_19.addWidget(self.label_11)

        self.comboBox_topK = PyComboBox(self.page_tools)
        self.comboBox_topK.addItem("")
        self.comboBox_topK.addItem("")
        self.comboBox_topK.addItem("")
        self.comboBox_topK.addItem("")
        self.comboBox_topK.addItem("")
        self.comboBox_topK.setObjectName(u"comboBox_topK")
        self.comboBox_topK.setMinimumSize(QSize(150, 30))
        self.comboBox_topK.setFont(font1)

        self.horizontalLayout_19.addWidget(self.comboBox_topK)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_19)

        self.btn_summary = PyPushButton(self.page_tools)
        self.btn_summary.setObjectName(u"btn_summary")
        self.btn_summary.setMinimumSize(QSize(150, 30))
        self.btn_summary.setFont(font1)

        self.horizontalLayout_14.addWidget(self.btn_summary)


        self.verticalLayout_12.addLayout(self.horizontalLayout_14)

        self.plainTextEdit = PyPlainTextEdit(self.page_tools)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout_12.addWidget(self.plainTextEdit)


        self.verticalLayout_5.addLayout(self.verticalLayout_12)


        self.verticalLayout_13.addLayout(self.verticalLayout_5)

        self.pages.addWidget(self.page_tools)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"CSCC-UJS-Apps", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Custom Widgets Page", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here will be all the custom widgets, they will be added over time on this page.\n"
"I will try to always record a new tutorial when adding a new Widget and updating the project on Patreon before launching on GitHub and GitHub after the public release.", None))
        self.prev_btn.setText("")
        self.stop_btn.setText("")
        self.next_btn.setText("")
        self.progress_label.setText(QCoreApplication.translate("MainPages", u"00:00", None))
        self.volume_btn.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("MainPages", u"\u8bbe\u7f6e", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainPages", u"api\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("MainPages", u"ASR API ENDPOINT", None))
        self.line_api_endpoint.setText(QCoreApplication.translate("MainPages", u"https://api.siliconflow.cn/v1/audio/transcriptions", None))
        self.label_4.setText(QCoreApplication.translate("MainPages", u"API KEY", None))
        self.line_api_key.setText(QCoreApplication.translate("MainPages", u"sk-", None))
        self.label_5.setText(QCoreApplication.translate("MainPages", u"MODEL NAME", None))
        self.line_model_name.setText(QCoreApplication.translate("MainPages", u"TeleAI/TeleSpeechASR", None))
        self.label_8.setText(QCoreApplication.translate("MainPages", u"REMOTE/LOCAL", None))
        self.toggle_local_remote.setText("")
        self.btn_apply.setText(QCoreApplication.translate("MainPages", u"\u5e94\u7528API", None))
        self.btn_check.setText(QCoreApplication.translate("MainPages", u"\u68c0\u6d4b\u8fde\u901a\u6027", None))
        self.label_status.setText(QCoreApplication.translate("MainPages", u"UNKOWN", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainPages", u"\u5b57\u5e55\u8bbe\u7f6e", None))
        self.label_12.setText(QCoreApplication.translate("MainPages", u"\u5b57\u5e55\u751f\u6210\u6a21\u578b", None))
        self.comboBox_sub_model.setItemText(0, QCoreApplication.translate("MainPages", u"funasr", None))
        self.comboBox_sub_model.setItemText(1, QCoreApplication.translate("MainPages", u"whisper", None))
        self.comboBox_sub_model.setItemText(2, QCoreApplication.translate("MainPages", u"api", None))

        self.label_13.setText(QCoreApplication.translate("MainPages", u"\u662f\u5426\u751f\u6210\u5b57\u5e55\u6587\u4ef6", None))
        self.toggle_save_subtitles.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("MainPages", u"\u4e3b\u9898", None))
        self.label_14.setText(QCoreApplication.translate("MainPages", u"\u5e94\u7528\u4e3b\u9898", None))
        self.comboBox_themes.setItemText(0, QCoreApplication.translate("MainPages", u"dark", None))
        self.comboBox_themes.setItemText(1, QCoreApplication.translate("MainPages", u"lignt", None))

        self.label_7.setText(QCoreApplication.translate("MainPages", u"\u89c6\u9891\u6587\u4ef6\u8def\u5f84", None))
        self.line_file.setText(QCoreApplication.translate("MainPages", u"\u5f53\u524d\u6587\u4ef6\u8def\u5f84", None))
        self.btn_file.setText(QCoreApplication.translate("MainPages", u"\u6d4f\u89c8...", None))
        self.btn_start_sub.setText(QCoreApplication.translate("MainPages", u"\u751f\u6210\u5b57\u5e55", None))
        self.btn_save_sub.setText(QCoreApplication.translate("MainPages", u"\u5bfc\u51fa\u5b57\u5e55", None))
        self.label_6.setText(QCoreApplication.translate("MainPages", u"\u542f\u7528\u7f16\u8f91", None))
        self.toggle_edit.setText("")
        self.label_3.setText(QCoreApplication.translate("MainPages", u"\u5b57\u5e55\u8f93\u51fa", None))
        self.label_9.setText(QCoreApplication.translate("MainPages", u"\u5173\u952e\u8bcd\u63d0\u53d6", None))
        self.label_15.setText(QCoreApplication.translate("MainPages", u"\u5173\u952e\u8bcd\u4e2a\u6570", None))
        self.comboBox_keynum.setItemText(0, QCoreApplication.translate("MainPages", u"1", None))
        self.comboBox_keynum.setItemText(1, QCoreApplication.translate("MainPages", u"2", None))
        self.comboBox_keynum.setItemText(2, QCoreApplication.translate("MainPages", u"3", None))
        self.comboBox_keynum.setItemText(3, QCoreApplication.translate("MainPages", u"4", None))

        self.btn_keyword.setText(QCoreApplication.translate("MainPages", u"\u63d0\u53d6\u5173\u952e\u8bcd", None))
        self.pushButton_3.setText("")
        self.pushButton_7.setText("")
        self.pushButton_8.setText("")
        self.pushButton_4.setText("")
        self.pushButton_10.setText("")
        self.pushButton_2.setText("")
        self.pushButton_9.setText("")
        self.pushButton_5.setText("")
        self.pushButton_1.setText("")
        self.pushButton_6.setText("")
        self.label_10.setText(QCoreApplication.translate("MainPages", u"\u6587\u672c\u6458\u8981", None))
        self.label_11.setText(QCoreApplication.translate("MainPages", u"\u6982\u62ec\u7cbe\u5ea6", None))
        self.comboBox_topK.setItemText(0, QCoreApplication.translate("MainPages", u"1", None))
        self.comboBox_topK.setItemText(1, QCoreApplication.translate("MainPages", u"2", None))
        self.comboBox_topK.setItemText(2, QCoreApplication.translate("MainPages", u"4", None))
        self.comboBox_topK.setItemText(3, QCoreApplication.translate("MainPages", u"8", None))
        self.comboBox_topK.setItemText(4, QCoreApplication.translate("MainPages", u"16", None))

        self.btn_summary.setText(QCoreApplication.translate("MainPages", u"\u63d0\u53d6\u6458\u8981", None))
    # retranslateUi

