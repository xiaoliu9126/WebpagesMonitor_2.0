import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import *
import json
# 引入ui设计
from UI_designer.home_window import Ui_home_Form
# 引入新的form-logic
from src.form_logic.MoodleCrawler import MoodleCrawler
from src.form_logic.Moodle import Moodle


class Forum_Window(QWidget, Ui_home_Form):
    def __init__(self, username, password, parent=None):
        super(Forum_Window, self).__init__(parent)
        self.setupUi(self)
        # 从爬虫中获取相应的课程信息
        self.getForumData()
        self.init_ui()
        self.init_slot()

    def init_ui(self):
        # 用toolbox实现按键显示效果
        self.forum_toolbox = QToolBox()
        self.forum_toolbox.layout().setSpacing(5)
        self.scrollArea.setWidget(self.forum_toolbox)
        # 我们将forum区分成重要以及不重要
        self.important_forum = []
        self.unimportant_forum = []
        for forum_item in self.forum_data['forum_data']:
            if forum_item['isimportant'] == 1 :
                self.important_forum.append(forum_item)
            else:
                self.unimportant_forum.append(forum_item)

        # 设置重要以及不重要groupBox框
        # 重要
        self.important_groupbox = QGroupBox()
        self.important_groupbox.setFixedSize(900, 500)
        self.important_groupbox_layout = QVBoxLayout()
        self.important_groupbox_layout.setAlignment(Qt.AlignCenter)
        self.important_groupbox.setLayout(self.important_groupbox_layout)

        #在groupbox里面添加课程信息

        for item in self.important_forum:
            self.important_course_layout = QHBoxLayout()
            self.important_course_layout.setStretch(0, 7)
            self.important_course_layout.setStretch(1, 3)
            # 定forum名称和link
            self.important_course_info_layout = QVBoxLayout()
            self.coursename = QLabel(item['discuss_title'])
            self.coursename.setProperty('class', 'Forum')
            self.courselink = QLabel(item['discuss_url'])
            self.courselink.setProperty('class', 'Forum')
            self.important_course_info_layout.addWidget(self.coursename)
            self.important_course_info_layout.addWidget(self.courselink)
            # 定义关注按钮
            self.isimportant_btn = QPushButton("不再关注")
            self.isimportant_btn.setProperty('class', 'Moodle')
            # 组合成一个layouy
            self.important_course_layout.addLayout(self.important_course_info_layout)
            self.important_course_layout.addWidget(self.isimportant_btn)


            # 我们添加了一条分割线
            self.line_1 = QFrame()
            self.line_1.setStyleSheet("background-color: rgb(222, 222, 222);")
            self.line_1.setFrameShape(QFrame.HLine)
            self.line_1.setFrameShadow(QFrame.Sunken)
            self.line_1.setObjectName("line_1")

            # 添加到groupbox中
            self.important_groupbox_layout.addWidget(self.line_1)
            self.important_groupbox_layout.addLayout(self.important_course_layout)

        # 不重要
        self.unimportant_groupbox = QGroupBox()
        self.unimportant_groupbox.setFixedSize(800, 500)
        self.unimportant_groupbox_layout = QVBoxLayout()
        self.unimportant_groupbox_layout.setAlignment(Qt.AlignCenter)
        self.unimportant_groupbox.setLayout(self.unimportant_groupbox_layout)

        self.forum_toolbox.addItem(self.important_groupbox, "重要")
        self.forum_toolbox.addItem(self.unimportant_groupbox, "不重要")


        # 添加qss效果
        self.setStyleSheet(SYS_STYLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle('Forum')

    def init_slot(self):
        print("")
        # self.moodle_listWidget.currentItemChanged.connect(self.item_changed)


    #从后端中提取forum信息
    def getForumData(self):
        # 创建Moodle对象，并实例化
        moodle = Moodle()
        # 用账号和密码模拟登录
        print(moodle.login("scyzz5", "Lxygwqfqsgct1s-"))
        # 创建MooldeCrawler对象，并实例化
        Crawler = MoodleCrawler(moodle)
        # TODO 当前将监督的课程设置成ACE，实际需要从moodle——window模块获取点击的监督的课程
        # 设置监视目标未ACE课程
        Crawler.set_current_page("https://moodle.nottingham.ac.uk/course/view.php?id=104761")
        # 获取ACE课程中全部讨论组和每个讨论组的内容
        forum_class = Crawler.get_forum()
        # forum_class[0]:Announcements Forum  forum_class[1]:Q&A forum
        # 我们选择announcements作为样例
        announcement_forum = forum_class[0]
        # 我们给forum添加一个额外的特征isimportant
        for forum_item in announcement_forum['forum_data']:
            # 初始化所有的forum为important
            forum_item['isimportant'] = 1

        self.forum_data = announcement_forum


    # session = newCnt("scyjw3" , "Wlwyhwjy199761&0827")
    # "username" = "scyzz5" "password" = "Lxygwqfqsgct1s-"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = 'scyzz5'
    password = 'Lxygwqfqsgct1s-'
    myWin = Forum_Window(username, password)
    myWin.show()
    sys.exit(app.exec_())