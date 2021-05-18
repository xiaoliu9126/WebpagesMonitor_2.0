import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import threading
from util.common_util import *
from UI_designer.setting_window import *
from src.moodle_spider import newCnt, getList, urlAnalysis

from src.monitor_window import *

class SettingWindow(QMainWindow, Ui_SettingWindow):
    # 创建登录成功与否的信号
    setting_signal = pyqtSignal(str)
    def __init__(self, isLoginMoodle, isLoginEmail, parent=None):
        super(SettingWindow, self).__init__(parent)
        self.setupUi(self)
        self.isloginMoodle = isLoginMoodle
        self.isloginEmail = isLoginEmail
        self.init_ui()
        self.init_slot()

    # def getData(self):
    #     # 从文件中获得相关课程信息
    #     user_course_path = os.path.join(USER_ALL_COURSE, 'data', self.username, 'all_course.json')
    #     print(user_course_path)
    #     if os.path.exists(user_course_path):
    #         print("已经存在用户文件夹")
    #         with open(user_course_path, 'r') as f:
    #             load_dict = json.load(f)
    #             num_course = len(load_dict)
    #             course_list = []
    #             for course in range(num_course):
    #                 courseName = load_dict[course]["courseName"]
    #                 courseUrl = load_dict[course]["courseUrl"]
    #                 course_dict = {'courseName': courseName, 'courseUrl': courseUrl}
    #                 course_list.append(course_dict)  # 依据列表的append对文件进行追加
    #             f.close()
    #
    #     else:
    #         print("没有该用信息，需要先登录获得该用户的信息")
    #
    #     self.data = course_list

    def init_ui(self):
        """
        初始化界面UI元素
        """
        self.setWindowTitle('Setting')
        self.setWindowIcon(QIcon(APP_ICON))
        # self.save_pushButton.setProperty('class', 'Aqua')
        # self.cancel_pushButton.setProperty('class', 'Aqua')
        # (1) 初始状态
        self.listWidget.setProperty('class', 'Normal')
        self.listWidget.setCurrentRow(0)
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)
        # General
        general_list_item = QListWidgetItem()
        general_list_item.setSizeHint(QSize(200, 80))
        gengeral_item_name = QLabel("General")
        gengeral_item_name.setStyleSheet("QLabel{color:rgb(0,0,205);font-size:18px;font-weight:normal;font-family:Arial;}")
        gengeral_item_name.setAlignment(Qt.AlignCenter)
        self.listWidget.addItem(general_list_item)
        self.listWidget.setItemWidget(general_list_item,gengeral_item_name)
        # 添加general对应的界面
        general_widget = QWidget()

        general_layout = QVBoxLayout()
        # a
        general_item_layout1 = QHBoxLayout()
        update_label = QLabel("Update time : ")
        update_edit = QLineEdit('')
        general_item_layout1.addWidget(update_label)
        general_item_layout1.addWidget(update_edit)
        general_layout.addLayout(general_item_layout1)

        # b
        general_item_layout2 = QHBoxLayout()
        Monitor_label = QLabel("Monitor interval : ")
        Monitor_edit = QLineEdit('')
        general_item_layout2.addWidget(Monitor_label)
        general_item_layout2.addWidget(Monitor_edit)
        general_layout.addLayout(general_item_layout2)

        # c
        general_item_layout3 = QHBoxLayout()
        self.cancel_ptn1 = QPushButton("Cancel")
        self.save_ptn1 = QPushButton("Save")

        self.cancel_ptn1.setProperty('class', 'Aqua')
        self.save_ptn1.setProperty('class', 'Aqua')

        general_item_layout3.addWidget(self.cancel_ptn1)
        general_item_layout3.addWidget(self.save_ptn1)
        general_layout.addLayout(general_item_layout3)

        general_widget.setLayout(general_layout)
        self.stackedWidget.addWidget(general_widget)

        # (2) Moodle
        if self.isloginMoodle:
            moodle_list_item = QListWidgetItem()
            moodle_list_item.setSizeHint(QSize(200, 80))
            moodle_item_name = QLabel("Moodle")
            moodle_item_name.setStyleSheet(
                "QLabel{color:rgb(0,0,205);font-size:18px;font-weight:normal;font-family:Arial;}")
            moodle_item_name.setAlignment(Qt.AlignCenter)
            self.listWidget.addItem(moodle_list_item)
            self.listWidget.setItemWidget(moodle_list_item, moodle_item_name)


            # 添加moodle对应的界面
            moodle_widget = QWidget()

            moodle_layout = QVBoxLayout()
            # a
            moodle_item_layout1 = QHBoxLayout()
            download_label = QLabel("Download path: ")
            download_edit = QLineEdit('')
            moodle_item_layout1.addWidget(download_label)
            moodle_item_layout1.addWidget(download_edit)
            moodle_layout.addLayout(moodle_item_layout1)

            # b
            moodle_item_layout2 = QHBoxLayout()
            self.change_monitor_ptn = QPushButton("Change monitor module")
            self.change_monitor_ptn.setProperty('class', 'Aqua')
            moodle_item_layout2.addWidget(self.change_monitor_ptn)
            moodle_layout.addLayout(moodle_item_layout2)

            # c
            moodle_item_layout3 = QHBoxLayout()
            self.logout_ptn2 = QPushButton("注销账号")
            self.cancel_ptn2 = QPushButton("Cancel")
            self.save_ptn2 = QPushButton("Save")

            self.logout_ptn2.setProperty('class', 'Aqua')
            self.cancel_ptn2.setProperty('class', 'Aqua')
            self.save_ptn2.setProperty('class', 'Aqua')

            moodle_item_layout3.addWidget(self.logout_ptn2)
            moodle_item_layout3.addWidget(self.cancel_ptn2)
            moodle_item_layout3.addWidget(self.save_ptn2)
            moodle_layout.addLayout(moodle_item_layout3)

            moodle_widget.setLayout(moodle_layout)
            self.stackedWidget.addWidget(moodle_widget)

        # (3) Email
        if self.isloginEmail:
            email_list_item = QListWidgetItem()
            email_list_item.setSizeHint(QSize(200, 80))
            email_item_name = QLabel("Email")
            email_item_name.setStyleSheet(
                "QLabel{color:rgb(0,0,205);font-size:18px;font-weight:normal;font-family:Arial;}")
            email_item_name.setAlignment(Qt.AlignCenter)
            self.listWidget.addItem(email_list_item)
            self.listWidget.setItemWidget(email_list_item, email_item_name)

            # 添加email对应的界面
            email_widget = QWidget()

            email_layout = QVBoxLayout()
            # a
            email_item_layout1 = QHBoxLayout()
            keywords_label = QLabel("Add key words : ")
            keywords_edit = QLineEdit('')
            email_item_layout1.addWidget(keywords_label)
            email_item_layout1.addWidget(keywords_edit)
            email_layout.addLayout(email_item_layout1)

            # b
            email_item_layout2 = QHBoxLayout()
            import_label = QLabel("Add important contact : ")
            import_edit = QLineEdit('')
            email_item_layout2.addWidget(import_label)
            email_item_layout2.addWidget(import_edit)
            email_layout.addLayout(email_item_layout2)

            # c
            email_item_layout3 = QHBoxLayout()
            re_keywords_label = QLabel("Remove key words : ")
            re_keywords_edit = QLineEdit('')
            email_item_layout3.addWidget(re_keywords_label)
            email_item_layout3.addWidget(re_keywords_edit)
            email_layout.addLayout(email_item_layout3)

            # d
            email_item_layout4 = QHBoxLayout()
            re_import_label = QLabel("Remove important contact : ")
            re_import_edit = QLineEdit('')
            email_item_layout4.addWidget(re_import_label)
            email_item_layout4.addWidget(re_import_edit)
            email_layout.addLayout(email_item_layout4)

            # c
            email_item_layout5 = QHBoxLayout()
            self.logout_ptn3 = QPushButton("注销账号")
            self.cancel_ptn3 = QPushButton("Cancel")
            self.save_ptn3 = QPushButton("Save")

            self.logout_ptn3.setProperty('class', 'Aqua')
            self.cancel_ptn3.setProperty('class', 'Aqua')
            self.save_ptn3.setProperty('class', 'Aqua')

            email_item_layout5.addWidget(self.logout_ptn3)
            email_item_layout5.addWidget(self.cancel_ptn3)
            email_item_layout5.addWidget(self.save_ptn3)
            email_layout.addLayout(email_item_layout5)

            email_widget.setLayout(email_layout)
            self.stackedWidget.addWidget(email_widget)


        self.setStyleSheet(SYS_STYLE)
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)

        # # 设置自动添加课程信息到combox
        # # 获取数据
        # self.course_list_data = self.data
        # for course_item_data in self.course_list_data:
        #     self.comboBox_3.addItem(course_item_data['courseName'])


    def init_slot(self):
        """
        初始化信号槽连接
        """
        self.listWidget.currentItemChanged.connect(self.item_changed)
        if self.isloginMoodle:
            self.logout_ptn2.clicked.connect(lambda: self.btn_slot('logout'))
            self.change_monitor_ptn.clicked.connect(lambda: self.btn_slot('change_monitor'))
        if self.isloginEmail:
            self.logout_ptn3.clicked.connect(lambda: self.btn_slot('logout'))

        # self.save_pushButton.clicked.connect(lambda: self.btn_slot('save'))
        # self.cancel_pushButton.clicked.connect(lambda: self.btn_slot('cancel'))

    def item_changed(self):
        if(self.listWidget.currentRow() == 0):
            self.stackedWidget.setCurrentIndex(self.listWidget.currentRow())

        if(self.listWidget.currentRow() == 1):
            self.stackedWidget.setCurrentIndex(self.listWidget.currentRow())

        if (self.listWidget.currentRow() == 2):
            self.stackedWidget.setCurrentIndex(self.listWidget.currentRow())



    def btn_slot(self, tag):
        """
        按钮点击事件槽函数
        :param tag: 点击的按钮的TAG
        :return: 出错返回,不执行后续操作逻辑
        """
        # logot
        if tag == 'logout':
            # 点击logout提示新窗口:当前账号文件将不被保留
            QMessageBox.information(self,  # 使用infomation信息框
                                    "警告",
                                    "当前账号文件将不被保留,是否继续注销!",
                                    QMessageBox.Yes | QMessageBox.No)
            # self.close()

        #change monitor
        if tag == 'change_monitor':
            # 弹出新窗口,为所有课程的复选框
            print("# 弹出新窗口,为所有课程的复选框")
            self.monitor_window = Monitor_Window()
            self.monitor_window.show()

        # 注册
        if tag == 'cancel':
            # 同时传递信息给主页面将moodle进行更新
            self.setting_signal.emit("Update")
            self.close()



        # 登陆
        if tag == 'save':
            update_time = self.comboBox_1.currentText()
            moniter_interval = self.comboBox_2.currentText()
            adding_monitor_modules = self.comboBox_3.currentText()
            moniter_area = self.comboBox_4.currentText()
            download_path = self.down_lineEdit.text()

            # 新建list作为信号传递
            setting_signal_list = []
            setting_signal_list.append({'update_time':update_time})
            setting_signal_list.append({'moniter_interval':moniter_interval})
            setting_signal_list.append({'adding_monitor_modules':adding_monitor_modules})
            setting_signal_list.append({'moniter_area':moniter_area})
            # 添加课程对应的link
            for course_item_data in self.course_list_data:
                if course_item_data['courseName'] == adding_monitor_modules:
                    course_item_url = course_item_data['courseUrl']
                    setting_signal_list.append({'course_item_url':course_item_url})

            # 如果download_path为空的话，则给他添加一个当前地址作为下载地址
            if download_path == '':
                new_download_path = os.path.join(USER_ALL_COURSE, 'data', self.username, adding_monitor_modules)
                setting_signal_list.append({'new_download_path': new_download_path})
            else:
                # ToDo 添加对下载路径的正确性判定
                new_download_path = os.path.join(download_path, adding_monitor_modules)
                setting_signal_list.append({'new_download_path': new_download_path})

            #TODO 存储成json文件夹
            courseinfofile(self, update_time, moniter_interval, adding_monitor_modules, moniter_area, course_item_url, new_download_path)
            # 同时传递信息给主页面将moodle进行更新
            self.setting_signal.emit("Update")
            self.close()

def courseinfofile(self, new_update_time, new_moniter_interval, new_adding_monitor_modules, new_moniter_area, new_course_item_url, new_new_download_path):
    user_monitoring_path = os.path.join(USER_ALL_COURSE, 'data', self.username) # 监控的课程存储信息
    if os.path.exists(user_monitoring_path):
        print("已经存在用户文件夹")
        user_monitoring_course_path = os.path.join(user_monitoring_path, 'monitoring_course.json')
        if (os.path.exists(user_monitoring_course_path)):
            with open(user_monitoring_course_path, 'r') as f:
                load_dict = json.load(f)
                num_course = len(load_dict)
                course_list = []
                for course in range(num_course):
                    update_time = load_dict[course]["update_time"]
                    moniter_interval = load_dict[course]["moniter_interval"]
                    adding_monitor_modules = load_dict[course]["adding_monitor_modules"]
                    moniter_area = load_dict[course]["moniter_area"]
                    course_item_url = load_dict[course]["course_item_url"]
                    new_download_path = load_dict[course]["new_download_path"]

                    course_dict = {'update_time': update_time, 'moniter_interval': moniter_interval,
                                   'adding_monitor_modules': adding_monitor_modules,
                                   'moniter_area': moniter_area, 'course_item_url': course_item_url,
                                   'new_download_path': new_download_path}
                    course_list.append(course_dict)  # 依据列表的append对文件进行追加
                f.close()
            # flag = 1 存在
            flag = 0
            for item in course_list:
                if item['adding_monitor_modules'] == new_adding_monitor_modules:
                    print("已经存在，不添加")
                    flag = 1
            if flag == 0:  # 不存在
                new_course_dict = {'update_time': new_update_time, 'moniter_interval': new_moniter_interval,
                                   'adding_monitor_modules': new_adding_monitor_modules,
                                   'moniter_area': new_moniter_area, 'course_item_url': new_course_item_url,
                                   'new_download_path': new_new_download_path}
                course_list.append(new_course_dict)

                with open(user_monitoring_course_path, 'w', encoding='utf-8') as file:
                    json.dump(course_list, file, ensure_ascii=False)
                    file.close()
        else:
            print("新建文件夹")
            course_list = []
            new_course_dict = {'update_time': new_update_time, 'moniter_interval': new_moniter_interval,
                               'adding_monitor_modules': new_adding_monitor_modules,
                               'moniter_area': new_moniter_area, 'course_item_url': new_course_item_url,
                               'new_download_path': new_new_download_path}
            course_list.append(new_course_dict)
            with open(user_monitoring_course_path, 'w', encoding='utf-8') as file:
                json.dump(course_list, file, ensure_ascii=False)
                file.close()
    else:
        print("该用户文件夹不存在需要登陆!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = SettingWindow(True,True)
    myWin.show()
    sys.exit(app.exec_())
