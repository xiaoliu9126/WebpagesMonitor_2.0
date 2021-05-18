"""
coding:utf-8
file: main_window.py
@desc: 主窗口
2.0.0 base 开发
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import *
import json
#引入操作逻辑
from src.home_window import HomeWindow
from src.moodle_window import MoodleWindow
from src.email_window import EmailWindow
from src.login_window import LoginWindow
from src.setting_window import SettingWindow

# 引入ui设计
from UI_designer.main import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #TODO get userinfo
        self.username = ''
        self.userpassword = ''
        self.isuserlogin = False  # = self.isloginmoodle
        self.isloginEmail = False
        # setting
        self.setupUi(self)
        self.init_slot()
        self.init_ui()
    def init_ui(self):
        # set WMR label size
        WMR_text = self.main_label_WMR
        WMR_text_pixmap = QPixmap(WMR_ICON)
        WMR_text.setPixmap(WMR_text_pixmap)
        WMR_text.setScaledContents(True)
        # set linedit icon
        search_action = QAction(self)
        search_action.setIcon(QIcon(SEARCH_ICON))
        search_action.triggered.connect(self.search)
        self.main_edit_search.addAction(search_action, QLineEdit.TrailingPosition)
        # set WMR icon
        WMR_label = self.main_label_icon
        WMR_pixmap = QPixmap(APP_ICON)
        WMR_label.setPixmap(WMR_pixmap)
        WMR_label.setScaledContents(True)
        # set left listWidget
        # 左侧没有星星图标需要修改图片绝对路径
        data = '[{"name":"Homepage", "icon":"E:/python_code/WebpagesMonitor_2.0/images/main_star.png"},' \
               '{"name":"Moodle", "icon":"E:/python_code/WebpagesMonitor_2.0/images/main_star.png"},' \
               '{"name":"Email", "icon":"E:/python_code/WebpagesMonitor_2.0/images/main_star.png"},' \
               '{"name":"Nusearch", "icon":"E:/python_code/WebpagesMonitor_2.0/images/main_star.png"},' \
               '{"name":"Google Scholar", "icon":"E:/python_code/WebpagesMonitor_2.0/images/main_star.png"},' \
               '{"name":"Setting", "icon":"E:/python_code/WebpagesMonitor_2.0/images/main_star.png"}]'
        listWidget_data = json.loads(data)
        self.listWidget.setProperty('class', 'Normal')
        self.listWidget.setCurrentRow(0)
        # 设置listwidget中每一个item的尺寸以及图标
        def get_item_wight(data):
            name = data['name']
            icon = data['icon']
            wight = QWidget()
            layout_main = QHBoxLayout()
            map_l = QLabel()  # icon显示
            map_l.setFixedSize(50, 50)
            maps = QPixmap(icon).scaled(50, 50)
            map_l.setPixmap(maps)
            item_name = QLabel(name)
            item_name.setStyleSheet("QLabel{color:rgb(0,0,205);font-size:18px;font-weight:normal;font-family:Arial;}")
            item_name.setAlignment(Qt.AlignCenter)
            layout_main.addWidget(map_l)
            layout_main.addWidget(item_name)
            wight.setLayout(layout_main)
            return wight

        for listWidget_item_data in listWidget_data:
            main_list_item = QListWidgetItem()
            main_list_item.setSizeHint(QSize(260, 80))
            main_list_widget = get_item_wight(listWidget_item_data)  # 调用上面的函数获取对应
            self.listWidget.addItem(main_list_item)  # 添加item
            self.listWidget.setItemWidget(main_list_item, main_list_widget)  # 为item设置widget

        #添加home window
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)
        self.home_window = HomeWindow(self.username, self.userpassword, self.isuserlogin)
        self.home_window.home_login_signal.connect(self.login_info)
        #添加Email window
        self.home_window.home_email_signal.connect(self.home_email_info)
        self.stackedWidget.addWidget(self.home_window)
        self.stackedWidget.addWidget(EmailWindow()) #我们设置EmailWindow的index=1

        self.setStyleSheet(SYS_STYLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle('WebpagesMonitor Robot 2.0.0 Beta')

    def init_slot(self):
        self.listWidget.currentItemChanged.connect(self.item_changed)

    def item_changed(self):
        if(self.listWidget.currentRow() == 0):
            self.stackedWidget.setCurrentIndex(self.listWidget.currentRow())

        if(self.listWidget.currentRow() == 1):
            # 问题1：添加功能判断当前是否有用户登陆
            if self.isuserlogin:
                print("User is login, opne moodle page")
                self.moodle_window = MoodleWindow(self.username, self.userpassword)
                self.stackedWidget.addWidget(self.moodle_window)
                self.stackedWidget.setCurrentIndex(2)
            else:
                print("User is not login, opne login page")
                self.moodle_login = LoginWindow()
                self.moodle_login.show()
                self.moodle_login.login_signal.connect(self.login_info)

        if(self.listWidget.currentRow() == 2):
            # Email 界面
            self.isloginEmail = True
            self.stackedWidget.setCurrentIndex(1)

        if(self.listWidget.currentRow() == 5):
            #(2)TODO 问题2：setting部分的UI设计
            # a.初始页面
            # b.初始化Moodle(不太明白该部分初始的意思,设计成登陆moodle之后)
            # c.初始化Email(同理)
            isloginMoodle = self.isuserlogin
            isloginEmail = self.isloginEmail
            self.moodle_setting = SettingWindow(isloginMoodle, isloginEmail)
            self.moodle_setting.show()

            # if self.isuserlogin:
            #
            #     print("你需要先登录")
            # else:
            #     username = self.userinfo.split(' ')[0]
            #     password = self.userinfo.split(' ')[1]
            #     self.moodle_setting = SettingWindow(username, password)
            #     self.moodle_setting.show()
            #     self.moodle_setting.setting_signal.connect(self.setting_info)

    def setting_info(self, info):
        if info == 'Update':
            print("设置过setting中需要监控的课程信息，从而更新moodle模块")
            username = self.userinfo.split(' ')[0]
            password = self.userinfo.split(' ')[1]
            if self.moodle_window:
                self.stackedWidget.removeWidget(self.moodle_window)
            self.moodle_window_2 = MoodleWindow(username, password)
            self.stackedWidget.insertWidget(2,self.moodle_window_2)
            self.stackedWidget.setCurrentIndex(2)
        else:
            print("没有更新setting，无需修改！")

    def login_info(self, username, userpassword, isuserlogin):
        if isuserlogin:
            # userinfo
            self.isuserlogin = isuserlogin
            self.username = username
            self.userpassword = userpassword
            # 添加Moodle界面 index=2
            self.moodle_window = MoodleWindow(username, userpassword)
            self.stackedWidget.addWidget(self.moodle_window)
            self.stackedWidget.setCurrentIndex(2)
        else:
            print("pass is error")


    # def home_moodle_info(self, info):
    #     if info == 'get Moodle':
    #         self.userinfo = info
    #         # 添加Moodle界面 index=2
    #         username = self.userinfo.split(' ')[0]
    #         password = self.userinfo.split(' ')[1]
    #         self.moodle_window = MoodleWindow(username, password)
    #         self.stackedWidget.addWidget(self.moodle_window)
    #         self.stackedWidget.setCurrentIndex(2)
    #     else:
    #         print("pass is error")

    def home_email_info(self, info):
        if info == 'get Email':
            # 我们设置EmailWindow的index=1
            self.isloginEmail = True
            self.stackedWidget.setCurrentIndex(1)


    def search(self):
        # 在这里添加搜索逻辑，输入课程名字会显示该课程相关信息到
        print("搜索")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
