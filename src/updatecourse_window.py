import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import *
import json
# 引入ui设计
from UI_designer.update_courselist import Ui_Form
# 引入新的form-logic
from src.form_logic.Controler import Controler
from src.form_logic.Moodle import Moodle


class Update_Window(QWidget, Ui_Form):
    def __init__(self, coursename, parent=None):
        super(Update_Window, self).__init__(parent)
        self.setupUi(self)
        self.coursename = coursename
        self.init_ui()
        self.init_slot()

    def init_ui(self):
        # init listwidget
        self.listWidget.setProperty('class', 'Normal')
        self.listWidget.setCurrentRow(0)
        # get course
        print("当前监督的课程")
        print(self.coursename)
        monitor_course = ''
        self.coursename_label.setText(self.coursename)
        #后端
        controler = Controler()
        print(controler.login("scyzz5", "Lxygwqfqsgct1s-", True))

        controler.delete_monitoring_course([2])
        controler.delete_monitoring_course([22])
        # controler.add_new_monitoring_course([1])

        # controler.delete_monitoring_course([5])
        listWidget_data = controler.scanning()
        for course_item in listWidget_data:
            if course_item['Name'] ==  self.coursename:
                monitor_course = course_item
        if monitor_course != '':
            self.monitor_coursenum = len(monitor_course['forum'])
            self.coursenum_label.setText("该课程forum更新数量:" + str(self.monitor_coursenum))
            if self.monitor_coursenum != 0:
                new_listWidget_data = monitor_course['forum'][0]
                self.coursenum_label.setText("该课程forum更新数量:" + str(new_listWidget_data['forum_data']))
                for listWidget_item_data in new_listWidget_data['forum_data']:
                    main_list_item = QListWidgetItem()
                    main_list_item.setSizeHint(QSize(500, 100))
                    main_list_widget = self.get_item_wight(listWidget_item_data)
                    self.listWidget.addItem(main_list_item)  # 添加item
                    self.listWidget.setItemWidget(main_list_item, main_list_widget)
        else:
            self.coursenum_label.setText("没有监督该课程")


        # 添加qss效果
        self.setStyleSheet(SYS_STYLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle('Monitor module')

    # 设置listwidget中每一个item的尺寸以及图标
    def get_item_wight(self, data):
        wight = QWidget()
        layout_main = QVBoxLayout()

        item_name = QLabel(data['discuss_title'])
        item_name.setStyleSheet("QLabel{color:rgb(0,0,205);font-size:18px;font-weight:normal;font-family:Arial;}")
        item_name.setAlignment(Qt.AlignCenter)

        layout_main.addWidget(item_name)

        # #(1) 课程 + 更新数量
        # course_layout1 = QHBoxLayout()
        # course_name_label = QLabel(course_name)
        # course_num_label = QLabel(str(update_course_num))
        # course_layout1.addWidget(course_name_label)
        # course_layout1.addWidget(course_num_label)

        # layout_main.addLayout(course_layout1)
            # (2) 更新的标题
            # "forum": [{"forum_name": "Announcements Forum", "forum_url": "https://moodle.nottingham.ac.uk/mod/forum/view.php?id=3330311", "forum_data": []}]}]
            # if update_course_num != 0:
            #     course_layout2 = QVBoxLayout()
            #     for forum_item in  data['forum']:
            #         item_name = QLabel(forum_item['forum_name'])
            #         item_name.setStyleSheet("QLabel{color:rgb(0,0,205);font-size:18px;font-weight:normal;font-family:Arial;}")
            #         item_name.setAlignment(Qt.AlignCenter)
            #         course_layout2.addWidget(item_name)
            #
            #     layout_main.addLayout(course_layout2)
        wight.setLayout(layout_main)
        return wight

    def init_slot(self):
        print("")
        # self.moodle_listWidget.currentItemChanged.connect(self.item_changed)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    course_name = 'Algorithms Correctness and Efficiency (COMP2048 UNNC) (FCH1 20-21)'
    myWin = Update_Window(course_name)
    myWin.show()
    sys.exit(app.exec_())