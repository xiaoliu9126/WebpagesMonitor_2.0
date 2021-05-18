import requests
from bs4 import BeautifulSoup
from src.form_logic.Url_json_list import url_and_json_info


# Moodle对象：
# Moodle对象专注于模拟登录，当对象被构造之后可以：
#   1. 调用login方法： 实现登录
#   2. 调用re_login方法：实现重新登陆
#   3. 调用set_username_and_password方法： 实现重新设置账号密码
#   4. 调用update_token方法： 获取并更新token，以保证正常登录
#   5. 调用update_sesskey方法： 获取并更新sesskey，结合session可以获取并下载Moodle全部信息
#   6. 调用log_out方法：退出登录
#   7. 调用test_connect方法：检查是否在登录状态

class Moodle:
    passData = {}  # 设置成private，提高安全性
    sesskey = None
    session = None

    # 初始化参数
    def __init__(self):
        self.passData["username"] = ""
        self.passData["password"] = ""
        self.passData["anchor"] = ""
        self.passData["logintoken"] = ""

        # 建立session对象
        self.session = requests.session()
        # 更新__passData参数
        self.__update_token()

    # 登录
    def login(self, username, password):
        self.set_username_and_password(username, password)
        # 登录
        if self.re_login():
            self.__update_sesskey()
            return True
        else:
            return False

    # 重新设置账号和密码
    def set_username_and_password(self, username, password):
        self.passData['username'] = username
        self.passData['password'] = password
        return True

    # 根据账号密码重新登录
    # 用于在session过期后，实现再次登陆
    # 若已经无需登录则返回False
    def re_login(self):
        if not self.__update_token():
            return False
        login = url_and_json_info.login_request_url
        html = self.session.post(login, data=self.passData).text
        bsObj = BeautifulSoup(html, 'lxml')
        if bsObj.find("title").text == "Dashboard":
            return True
        else:
            print("Fail to login, error code: 101")
            return False

    # 退出登录
    def log_out(self):
        log_out = url_and_json_info.log_out_request_url + str(self.sesskey)
        # print(log_out)
        self.session.get(log_out)
        if self.sesskey is not None:
            return True
        else:
            return False

    # 检查是否在登录状态
    def test_connect(self):
        home_page = url_and_json_info.home_page_url
        html = self.session.get(home_page).text
        bsObj = BeautifulSoup(html, 'lxml')
        if bsObj.find("title").text == "Dashboard":
            return True
        else:
            return False

    # 获取并更新token，以保证正常登录
    # 若已经登录，本方法将会返回False
    def __update_token(self):
        login = url_and_json_info.login_request_url

        login_page_html = self.session.get(login)
        bsObj = BeautifulSoup(login_page_html.text, "lxml")  # need install lxml (> pip install lxml)
        if (bsObj.find("form", {'class': 'loginform'})) is not None:
            token = bsObj.find("form", {'class': 'loginform'}).find("input", {'name': 'logintoken'}).attrs['value']
        else:
            print("You has login, error code: 102")
            return False
        self.passData['logintoken'] = token
        return True

    # 登录成功后获取并更新sesskey，结合session可以获取并下载Moodle全部信息
    def __update_sesskey(self):
        HomeUrl = url_and_json_info.home_page_url

        home_page_html = self.session.get(HomeUrl)
        bsObj = BeautifulSoup(home_page_html.text, 'lxml')
        if bsObj.find("input", {'name': 'sesskey'}) is not None:
            self.sesskey = bsObj.find("input", {'name': 'sesskey'}).attrs['value']
            return True
        else:
            print("Can not get sesskey, error code: 103")
            return False


# 测试
if __name__ == '__main__':
    # 实例化Moodle对象
    moodle = Moodle()
    # 用用户名和密码登录
    print(moodle.login("scyzz5", "Lxygwqfqsgct1s-"))
    # 在已经登录的条件下，运行重新登陆方法
    print(moodle.re_login())
    # 退出登录
    print(moodle.log_out())
    # 在退出登陆的条件下，运行重新登录方法
    print(moodle.re_login())
    # 检查是否处于连接状态
    print(moodle.test_connect())
