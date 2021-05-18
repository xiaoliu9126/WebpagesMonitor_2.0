import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.common_util import APP_ICON, SYS_STYLE
import json
from src.email_spider import newEmail
from src.show_email_window import ShowEmailWindow
# 引入ui设计
from UI_designer.home_window import Ui_home_Form
import zmail

class EmailWindow(QWidget, Ui_home_Form):
    def __init__(self, parent=None):
        super(EmailWindow, self).__init__(parent)
        self.setupUi(self)
        self.getEmail()
        self.init_ui()


    def getEmail(self):
        server = newEmail("", "")
        # 获取所有的邮件
        self.mails = server.get_mails()

    def init_ui(self):
        # 用toolbox实现按键显示效果
        self.email_toolbox = QToolBox()
        self.email_toolbox.layout().setSpacing(5)
        self.scrollArea.setWidget(self.email_toolbox)
        # toolbox 包含内容
        self.data = ['Key Words', 'Marked Contacts', 'Others']
        # 获取数据
        for email_item_data in self.data:
            self.email_groupbox = QGroupBox()
            self.email_groupbox.setFixedSize(600, 180)
            self.email_groupbox_layout = QVBoxLayout()
            self.email_groupbox_layout.setAlignment(Qt.AlignCenter)
            self.email_groupbox.setLayout(self.email_groupbox_layout)

            for email in self.mails:
                #按钮上的字是要传递信息的
                self.button_text = str(email['id'])+' '+email['from']
                self.moodle_btn = QPushButton(self.button_text)
                # self.moodle_btn.setText(email['from'])
                self.moodle_btn.setFixedSize(500, 40)
                self.moodle_btn.setProperty('class', 'Moodle')
                self.moodle_btn.clicked.connect(lambda: self.btn_email(self.sender().text()))
                self.email_groupbox_layout.addWidget(self.moodle_btn)
            self.email_toolbox.addItem(self.email_groupbox, email_item_data)

    def btn_email(self, email_text):
        email_index = email_text.split(' ')[0]
        for email in self.mails:
            if email_index == str(email['id']):
                self.showemail_window = ShowEmailWindow()
                self.showemail_window.announcelabel.setText(email['subject'])
                self.showemail_window.anntimelabel.setText(email['from'])
                self.showemail_window.announcetextEdit.setText(str(email['content_text']))
                self.showemail_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = EmailWindow()
    myWin.show()
    sys.exit(app.exec_())



