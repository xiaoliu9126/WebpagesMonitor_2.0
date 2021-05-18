import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import *
import json
#引入操作逻辑
from src.login_window import LoginWindow
# from src.email_window import EmailWindow
from src.moodle_window import MoodleWindow
# 引入ui设计
from UI_designer.home_window import Ui_home_Form
#引入后端逻辑以及操作
from src.form_logic.Moodle import *

class HomeWindow(QWidget, Ui_home_Form):
    # 创建登录成功与否的信号
    home_login_signal = pyqtSignal(str, str, bool)
    # 自定义信号
    home_email_signal = pyqtSignal(str)
    def __init__(self, username, userpassword, isuserlogin, parent=None):
        super(HomeWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.username = username
        self.userpassword = userpassword
        self.isuserlogin = isuserlogin
    def init_ui(self):
        #QToolButton()
        self.home_grid_Layout = QGridLayout()
        self.home_button_1 = QToolButton()
        self.home_button_1.setProperty('class', 'home')
        self.home_button_1.setFixedSize(160,160)
        self.home_button_1.setText("HomePage")
        self.home_button_1.setIcon(QIcon(START_ICON))
        self.home_button_1.setIconSize(QSize(60, 60))
        self.home_button_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.home_button_2 = QToolButton()
        self.home_button_2.setProperty('class', 'home')
        self.home_button_2.setFixedSize(160, 160)
        self.home_button_2.setText("Moodle")
        self.home_button_2.setIcon(QIcon(START_ICON))
        self.home_button_2.setIconSize(QSize(60, 60))
        self.home_button_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.home_button_3 = QToolButton()
        self.home_button_3.setProperty('class', 'home')
        self.home_button_3.setFixedSize(160, 160)
        self.home_button_3.setText("Email")
        self.home_button_3.setIcon(QIcon(START_ICON))
        self.home_button_3.setIconSize(QSize(60, 60))
        self.home_button_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.home_button_4 = QToolButton()
        self.home_button_4.setProperty('class', 'home')
        self.home_button_4.setFixedSize(160, 160)
        self.home_button_4.setText("Setting")
        self.home_button_4.setIcon(QIcon(START_ICON))
        self.home_button_4.setIconSize(QSize(60, 60))
        self.home_button_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.home_grid_Layout.addWidget(self.home_button_1, 0, 0)
        self.home_grid_Layout.addWidget(self.home_button_2, 0, 1)
        self.home_grid_Layout.addWidget(self.home_button_3, 0, 2)
        self.home_grid_Layout.addWidget(self.home_button_4, 1, 0)
        self.scrollArea.setLayout(self.home_grid_Layout)
        self.setStyleSheet(SYS_STYLE)

        self.home_button_2.clicked.connect(self.Moodle)
        self.home_button_3.clicked.connect(self.Email)

    # 添加按钮功能
    def Moodle(self):
        # 问题1：添加功能判断当前是否有用户登陆
        if self.isuserlogin:
            print("User is login, opne moodle page")
            self.home_login_signal.emit(self.username, self.userpassword, self.isuserlogin)
            # self.moodle_login.login_signal.connect(self.home_login_info)
            # self.moodle_window = MoodleWindow(self.username, self.userpassword)
            # self.stackedWidget.addWidget(self.moodle_window)
            # self.stackedWidget.setCurrentIndex(2)
        else:
            print("User is not login, opne login page")
            self.moodle_login = LoginWindow()
            self.moodle_login.show()
            self.moodle_login.login_signal.connect(self.home_login_info)


        #
        # print("login for moodle")
        # self.login_window = LoginWindow()
        # self.login_window.show()
        # # 登陆成功
        # self.login_window.login_signal.connect(self.login_info)

    def home_login_info(self, username, userpassword, isuserlogin):
        if isuserlogin:
            # userinfo
            self.isuserlogin = isuserlogin
            self.username = username
            self.userpassword = userpassword
            # 添加Moodle界面 index=2
            self.home_login_signal.emit(username, userpassword, isuserlogin)
        else:
            print("pass is error")
            self.home_login_signal.emit("", "", False)


    def Email(self):
        print("Email")
        # self.stackedWidget.setCurrentIndex(self.listWidget.currentRow())
        self.home_email_signal.emit('get Email')



