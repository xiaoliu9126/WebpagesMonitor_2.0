import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import APP_ICON, SYS_STYLE, msg_box
import os
import json
import threading
from util.common_util import *
#引入UI逻辑
from UI_designer.login_window import *
#引入爬虫逻辑
from src.moodle_spider import newCnt, getList, urlAnalysis
#引入后端逻辑以及操作
from src.form_logic.Controler import *

class LoginWindow(QWidget, Ui_LoginForm):
    # 创建登录成功与否的信号，并且通过这些信息传递帐号+密码
    login_signal = pyqtSignal(str, str, bool)
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        # ADD Moodle logic
        self.moodle_controler = Controler()

    def init_ui(self):
        """
        初始化界面UI元素
        """
        self.setWindowTitle('login for moodel')
        self.setWindowIcon(QIcon(APP_ICON))
        self.login_pushButton.setProperty('class', 'Aqua')
        self.register_pushButton.setProperty('class', 'Aqua')
        self.setStyleSheet(SYS_STYLE)
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)

    def init_slot(self):
        """
        初始化信号槽连接
        """
        self.register_pushButton.clicked.connect(lambda: self.btn_slot('cancel'))
        self.login_pushButton.clicked.connect(lambda: self.btn_slot('login'))
        # self.login_done_signal.connect(self.handle_login)

    def btn_slot(self, tag):
        """
        按钮点击事件槽函数
        :param tag: 点击的按钮的TAG
        :return: 出错返回,不执行后续操作逻辑
        """

        # cancel
        if tag == 'cancel':
            # 关闭登陆界面
            self.close()

        # ok
        if tag == 'login':
            username = self.username_lineEdit.text()
            password = self.password_lineEdit.text()
            if '' in [username, password]:
                msg_box(self, '提示', '请输入用户名或密码!')
                return

            #获得输入的账户名和密码
            # "username" = "scyzz5"
            # "password" = "Lxygwqfqsgct1s-"

            # 用户名scyjw3
            # 密码Wlwyhwjy9761 & 20000827


            print("username: " + username + ",password： " + password)
            # 判断该用户是否登录成功
            isuserlogin = self.moodle_controler.login(username, password, True)
            if isuserlogin:
                print("Login sucess!\n")
                # 将登录信息传递给主页面
                self.login_signal.emit(username, password, isuserlogin)
                # 进入moodle界面
                self.close()
            else:
                print("Login fail!\n")
                self.login_signal.emit('','',False)
                QMessageBox.about(self, "ERROR", "密码或者账号发生错误！")
            # # 爬虫爬取课程信息
            # new_session = newCnt(username, password)
            # login_mess = username + " " + password
            # if new_session:
            #     print("Login sucess!\n")
            #     # 将登录信息传递给主页面
            #     self.login_signal.emit(login_mess)
            #     # 进入moodle界面
            #     self.close()
            #     # 同时获取所有课程信息的列表存储到文件中
            #     downuser_allcourse = threading.Thread(target=down_course, args=(new_session, username))  # 通过target指定子线程要执行的任务。可以通过args=元组 来指定test1的参数。
            #     downuser_allcourse.start()  # 只有在调用start方法后才会创建子线程并执行
            #     # all_courselist = getList(new_session)
            #     print("")
            # else:
            #     print("Login fail!\n")
            #     self.login_signal.emit('')
            #     QMessageBox.about(self, "ERROR", "密码或者账号发生错误！")

def down_course(session, username):
    print("将该用户的所有课程信息存储到文件夹中")
    all_courselist = getList(session)
    user_path = os.path.join(USER_ALL_COURSE, 'data', username)
    if os.path.exists(user_path):
        print("已经存在用户文件夹")
        user_course_path = os.path.join(user_path, 'all_course.json')
        with open(user_course_path, 'w', encoding='utf-8') as file:
            json.dump(all_courselist, file, ensure_ascii=False)
            file.close()
    else:
        print("新建该用户文件夹")
        os.makedirs(user_path)
        user_course_path = os.path.join(user_path, 'all_course.json')
        with open(user_course_path, 'w', encoding='utf-8') as file:
            json.dump(all_courselist, file, ensure_ascii=False)
            file.close()
    print("文件写入完成")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = LoginWindow()
    myWin.show()
    sys.exit(app.exec_())
