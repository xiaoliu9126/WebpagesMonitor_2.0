import sys,webbrowser
from PyQt5.QtGui import QIcon,QFont,QDesktopServices
from PyQt5.QtCore import Qt,QSize,QUrl
from PyQt5.QtWidgets import QApplication, QToolBox, QGroupBox, QToolButton, QVBoxLayout


class Demo(QToolBox):  # 1
    def __init__(self):
        super(Demo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,400,320)
        self.setWindowTitle("QToolBox抽屉窗口")
        self.layout_init()

    def layout_init(self):
        self.groupBox1 = QGroupBox("搜索", self)
        self.groupBox2 = QGroupBox("视频", self)
        self.groupBox3 = QGroupBox("购物", self)

        self.vboxLayout1 = QVBoxLayout()
        self.vboxLayout2 = QVBoxLayout()
        self.vboxLayout3 = QVBoxLayout()
        self.toolButton_Icons = ["百度.png","谷歌.png","搜狐.png", "土豆.png","优酷.png","bilibili.png","淘宝.png","京东.png","亚马逊.png","唯品会.png","返利.png"]
        self.toolButton_Names = ["百度搜索","谷歌搜索","搜狐视频","土豆视频","优酷视频","bilibili番剧","淘宝","京东","亚马逊","唯品会","返利"]
        self.toolButtons = []
        for i in range(len(self.toolButton_Icons)):
            toolButton = QToolButton(self)
            toolButton.setIcon(QIcon(self.toolButton_Icons[i]))
            toolButton.setIconSize(QSize(80,80))
            toolButton.setText(self.toolButton_Names[i])
            toolButton.setFont(QFont("微软雅黑",16,QFont.Bold))
            toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            toolButton.setAutoRaise(True)
            toolButton.clicked.connect(self.btnClicked)
            self.toolButtons.append(toolButton)
            if i<2:
                self.vboxLayout1.addWidget(toolButton)
                self.vboxLayout1.setAlignment(Qt.AlignCenter)
            elif i<6:
                self.vboxLayout2.addWidget(toolButton)
                self.vboxLayout2.setAlignment(Qt.AlignCenter)
            else:
                self.vboxLayout3.addWidget(toolButton)
                self.vboxLayout3.setAlignment(Qt.AlignCenter)

        # self.groupBox1.setFlat(True)  #将groupBox 设置为flat
        # self.groupBox2.setFlat(True)
         # self.groupBox3.setFlat(True)
        self.groupBox1.setLayout(self.vboxLayout1)
        self.groupBox2.setLayout(self.vboxLayout2)
        self.groupBox3.setLayout(self.vboxLayout3)

        self.addItem(self.groupBox1,"搜索引擎！")
        self.addItem(self.groupBox2,"视频网站！")
        self.addItem(self.groupBox3,"购物网站！")

        self.currentChanged.connect(self.print_index_func)


    def print_index_func(self):
        toolboxs = {
            0:"搜索引擎！",
            1:"视频网站！",
            2:"购物网站！"
        }
        sentence = "你选择的栏目是：{}".format(toolboxs.get(self.currentIndex()))
        print(sentence)

    def btnClicked(self):
        urls_info = {"百度搜索": "https://www.baidu.com/", "谷歌搜索":"https://www.google.com.hk/",
                    "搜狐视频":"https://tv.sohu.com/", "土豆视频":"http://www.tudou.com/", "优酷视频":"http://www.youku.com/", "bilibili番剧":"https://www.bilibili.com/",
                    "淘宝":"https://www.taobao.com/", "京东": "https://www.jd.com/", "亚马逊":"https://www.amazon.cn/","唯品会":"https://www.vip.com/","返利":"https://www.fanli.com/"
        }
        items = [item for item in urls_info.items()]
        for i in range(len(items)):
            if self.sender().text() == items[i][0]:
                QDesktopServices.openUrl(QUrl(items[i][1]))
                # webbrowser.open(items[i][1]))     #导入webbrowser模块，与上述调用QDesktopServices,QUrl 效果一样打开网页

if __name__ == '__main__':
     app = QApplication(sys.argv)
     demo = Demo()
     demo.show()
     sys.exit(app.exec_())
QToolBox()+QToolButton()