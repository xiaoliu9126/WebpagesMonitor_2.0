import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import threading
from util.common_util import APP_ICON, SYS_STYLE, msg_box
from UI_designer.announce_window import *
from src.moodle_spider import newCnt, getList, urlAnalysis

class ShowEmailWindow(QWidget, Ui_AnnounceForm):
    def __init__(self, parent=None):
        super(ShowEmailWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        """
        初始化界面UI元素
        """
        self.setWindowTitle('ShowEmailWindow')
        self.setWindowIcon(QIcon(APP_ICON))
        self.setStyleSheet(SYS_STYLE)
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)

