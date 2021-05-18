import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import *
import json
# 引入ui设计
from UI_designer.monitor_window import Ui_Monitor_Form
# 引入新的form-logic
from src.form_logic.Controler import Controler
from src.form_logic.Moodle import Moodle


class Monitor_Window(QWidget, Ui_Monitor_Form):
    def __init__(self,parent=None):
        super(Monitor_Window, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.init_slot()

    def init_ui(self):
        # init listwidget
        self.listWidget.setProperty('class', 'Normal')
        self.listWidget.setCurrentRow(0)
        # get course

        controler = Controler()
        controler.login("scyzz5", "Lxygwqfqsgct1s-", True)
        listWidget_data = controler.show_all_courses()

        for listWidget_item_data in listWidget_data:
            main_list_item = QListWidgetItem()
            # main_list_item.setSizeHint(QSize(260, 80))
            # QCheckBox
            course_checkbox = QCheckBox(listWidget_item_data['course_name'])
            self.listWidget.addItem(main_list_item)  # 添加item
            self.listWidget.setItemWidget(main_list_item, course_checkbox)

        self.monitor_ptn_cancel.setProperty('class', 'Aqua')
        self.monitor_ptn_save.setProperty('class', 'Aqua')

        # 添加qss效果
        self.setStyleSheet(SYS_STYLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle('Monitor module')

    def init_slot(self):
        print("")
        # self.moodle_listWidget.currentItemChanged.connect(self.item_changed)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Monitor_Window()
    myWin.show()
    sys.exit(app.exec_())