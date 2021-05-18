import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import *
import json
import threading
# 引入爬虫设计
from src.moodle_spider import newCnt, getList, urlAnalysis, downAnnouncements, downForum
# 引入ui设计
from UI_designer.home_window import Ui_home_Form
from src.announce_window import AnnounceWindow
from src.updatecourse_window import Update_Window
# 引入新的form-logic
from src.form_logic.MoodleCrawler import MoodleCrawler
from src.form_logic.Moodle import Moodle


class MoodleWindow(QWidget, Ui_home_Form):
    def __init__(self, username, password, parent=None):
        super(MoodleWindow, self).__init__(parent)
        self.setupUi(self)
        self.username = username
        self.password = password
        self.getSession()
        # 从爬虫中获取相应的课程信息
        # self.getCourseData()
        self.init_ui()
        self.init_slot()

    def getSession(self):
        # 从爬虫中爬取数据
        self.session = newCnt(self.username, self.password)
        # 得到数据
        user_monitoring_path = os.path.join(USER_ALL_COURSE, 'data', self.username)  # 监控的课程存储信息
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
                self.data = course_list
        else:
            print("该用户文件夹不存在需要登陆!")
            self.data = []


    def init_ui(self):
        # 用toolbox实现按键显示效果
        self.moodle_toolbox = QToolBox()
        self.moodle_toolbox.layout().setSpacing(5)
        self.scrollArea.setWidget(self.moodle_toolbox)
        # 获取数据
        for course_item_data in self.data:
            self.moodle_groupbox = QGroupBox()
            self.moodle_groupbox.setFixedSize(600,180)
            self.moodle_groupbox_layout = QVBoxLayout()
            self.moodle_groupbox_layout.setAlignment(Qt.AlignCenter)
            self.moodle_groupbox.setLayout(self.moodle_groupbox_layout)

            self.moodle_btn_1 = QPushButton()
            self.moodle_btn_1.setText("New Class Material")
            self.moodle_btn_1.setFixedSize(450, 50)
            self.moodle_btn_1.setProperty('class', 'Moodle')
            self.moodle_btn_1.clicked.connect(lambda: self.btn1(self.moodle_toolbox.currentIndex()))

            self.moodle_btn_2 = QPushButton()
            self.moodle_btn_2.setText("Forum updates")
            self.moodle_btn_2.setFixedSize(450, 50)
            self.moodle_btn_2.setProperty('class', 'Moodle')
            self.moodle_btn_2.clicked.connect(lambda: self.btn2(self.moodle_toolbox.currentIndex()))

            self.moodle_btn_3 = QPushButton()
            self.moodle_btn_3.setText("Announcement Updates")
            self.moodle_btn_3.setFixedSize(450, 50)
            self.moodle_btn_3.setProperty('class', 'Moodle')
            self.moodle_btn_3.clicked.connect(lambda: self.btn3(self.moodle_toolbox.currentIndex()))

            self.moodle_groupbox_layout.addWidget(self.moodle_btn_1)
            self.moodle_groupbox_layout.addWidget(self.moodle_btn_2)
            self.moodle_groupbox_layout.addWidget(self.moodle_btn_3)

            self.moodle_toolbox.addItem(self.moodle_groupbox, course_item_data['adding_monitor_modules'])

        # 添加qss效果
        self.setStyleSheet(SYS_STYLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle('Moodle')

    def init_slot(self):
        print("")
        # self.moodle_listWidget.currentItemChanged.connect(self.item_changed)

    # TODO Check 问题4
    # 该部分是下载文件部分
    # 该部分问题的产生是因为在下载OSC课程的时候,将文件的路径指向OSC文件夹;再次下载ACE文件则会造成文件夹缺失
    # 当前解决方式(1)每次下载文件的时候重新将文件夹指向到根目录文件(2)更好的建议将下载并入后端中进行重新设计修改
    def btn1(self, current_index):
        self.courseName = self.data[current_index]['adding_monitor_modules']
        self.courseUrl = self.data[current_index]['course_item_url']
        # down pdf
        downpdf = threading.Thread(target=downfile, args=(self.session,self.courseName,self.courseUrl))  # 通过target指定子线程要执行的任务。可以通过args=元组 来指定test1的参数。
        downpdf.start()  # 只有在调用start方法后才会创建子线程并执行


    # TODO Check 问题6 需要的是距离上次提醒和新的这次提醒的这段时间内所有的更新信息
    def btn2(self, current_index):
        #Moodle部分课程显示被监督的课程列表,但是当前并没有将后端逻辑与UI链接,建议进行修改

        # 将当前课程名字进行传递(建议修改成课程编号)
        self.courseName = self.data[current_index]['adding_monitor_modules']
        self.update_window = Update_Window(self.courseName)
        self.update_window.show()

        # self.courseName = self.data[current_index]['adding_monitor_modules']
        # self.courseUrl = self.data[current_index]['course_item_url']
        #
        # print("下载Forum")
        # self.forumfilename = downForum(self.session, self.username, self.courseName, self.courseUrl)
        # self.announcements_window = AnnounceWindow()
        # user_announcement_folder = os.path.join(USER_ALL_COURSE, 'data', self.username, "Forum")
        # if os.path.exists(user_announcement_folder):
        #     user_announcement_path = os.path.join(user_announcement_folder, self.forumfilename)
        # else:
        #     os.makedirs(user_announcement_folder)
        #     user_announcement_path = os.path.join(user_announcement_folder, self.forumfilename)
        #
        # with open(user_announcement_path, 'r', encoding='utf-8') as f:
        #     load_dict = json.load(f)
        #     # 得到最新的公告
        #     subject = load_dict[0]['subject']
        #     time = load_dict[0]['time']
        #     context = load_dict[0]['context']
        #     f.close()
        # self.announcements_window.announcelabel.setText(subject)
        # self.announcements_window.anntimelabel.setText(time)
        # self.announcements_window.announcetextEdit.setText(context)
        # self.announcements_window.show()

    def btn3(self, current_index):
        # 展示相关课程的announcement
        self.courseName = self.data[current_index]['adding_monitor_modules']
        self.courseUrl = self.data[current_index]['course_item_url']
        # down announcement
        print("下载announcement")
        self.announcefilename = downAnnouncements(self.session, self.username, self.courseName, self.courseUrl)
        print("传递信息给子窗口")
        self.announcements_window = AnnounceWindow()
        # 在主页面给子页面添加一些数据
        print("打开announcement window")
        ##### 不显示课程公告修改这个路径
        user_announcement_folder = os.path.join(USER_ALL_COURSE, 'data', self.username, "Announcement")
        if os.path.exists(user_announcement_folder):
            user_announcement_path = os.path.join(user_announcement_folder, self.announcefilename)
        else:
            os.makedirs(user_announcement_folder)
            user_announcement_path = os.path.join(user_announcement_folder, self.announcefilename)

        with open(user_announcement_path, 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
            # 得到最新的公告
            subject = load_dict[0]['subject']
            time = load_dict[0]['time']
            context = load_dict[0]['context']
            f.close()
        self.announcements_window.announcelabel.setText(subject)
        self.announcements_window.anntimelabel.setText(time)
        self.announcements_window.announcetextEdit.setText(context)
        self.announcements_window.show()

def downfile(session, courseName, courseUrl):
    print("下载文件啦...")
    print(courseName)
    print(courseUrl)
    urlAnalysis(session, courseName, courseUrl)


    # session = newCnt("scyjw3" , "Wlwyhwjy199761&0827")
    # "username" = "scyzz5" "password" = "Lxygwqfqsgct1s-"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = 'scyzz5'
    password = 'Lxygwqfqsgct1s-'
    myWin = MoodleWindow(username,password)
    myWin.show()
    sys.exit(app.exec_())