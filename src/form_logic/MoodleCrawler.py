import re

from bs4 import BeautifulSoup
from src.form_logic.Moodle import Moodle
from src.form_logic.Url_json_list import url_and_json_info


class MoodleCrawler:
    moodle = None
    __page_html = None
    __bsObj = None

    # 初始化，将带有session的Moodle类传入
    def __init__(self, moodle):
        self.moodle = moodle

    # 设置目标网址，一定要传入某个的url
    # 即 get_list 方法运行后返回的 url
    def set_current_page(self, url):
        self.__page_html = self.moodle.session.get(url).text
        self.__bsObj = BeautifulSoup(self.__page_html, 'lxml')

    # Warning： 在 set_current_page() 后运行
    # 获取网页中所有文件夹，并提供链接
    def get_folder(self):  # 存储folder名与其链接
        Folder = []
        temp = {}
        bsObj = self.__bsObj
        # print(bsObj.decode('utf-8'))
        folderUrl = bsObj.findAll("a", href=re.compile(".*((/mod/)(folder))"))
        print("There are " + str(len(folderUrl)) + " Folder in this web")
        for link in folderUrl:
            if 'href' in link.attrs:
                if 'instancename' in link.span.attrs['class']:
                    temp = {}
                    temp['folder_name'] = link.span.text
                    temp['folder_url'] = link.attrs['href']
                    Folder.append(temp)
        return Folder

    # Warning： 在 set_current_page() 后运行
    # 获取网页中所有内部链接，检查是否是文件（可下载的），如果是文件，则储存下载url（直接点击下载）
    def get_inner_link(self):
        inner_link = []
        bsObj = self.__bsObj
        # print(bsObj.decode('utf-8'))
        inner_link_url = bsObj.findAll("a", href=re.compile(".*((/mod/)[(resource)(url)])"))
        print("There are " + str(len(inner_link_url)) + " inner link in this web")
        for link in inner_link_url:
            if 'href' in link.attrs:
                if 'instancename' in link.span.attrs['class']:
                    temp = {}
                    temp['inner_link_name'] = link.span.text
                    temp['inner_link_url'] = link.attrs['href']
                    temp['inner_link_downloadable'] = False
                    temp['inner_link_download_url'] = []
                    img = link.find("img", src=re.compile(".*(/f/)"))
                    if img is not None:
                        temp['inner_link_downloadable'] = True
                    if temp['inner_link_downloadable']:
                        download_page = self.moodle.session.get(temp['inner_link_url']).text
                        bsObj = BeautifulSoup(download_page, 'lxml')
                        inner_link_download_url = bsObj.findAll("a", href=re.compile(".*(pluginfile)"))
                        for i in inner_link_download_url:
                            temp['inner_link_download_url'].append(i.attrs['href'])
                    inner_link.append(temp)
        return inner_link

    # Warning： 在 set_current_page() 后运行
    # 获取网页中所有外部链接（扩展阅读等等老师上传的连接），保存链接和名字
    def get_outer_link(self):
        outer_link = []
        bsObj = self.__bsObj
        outer_link_url = bsObj.findAll("a", href=re.compile(
            "^((?!nottingham)(?!moodle).)*http((?!nottingham)(?!moodle).)*$"))
        print("There are " + str(len(outer_link_url)) + " outer link in this web")
        for link in outer_link_url:
            temp = {}
            temp['outer_link_name'] = link.text
            temp['outer_link_url'] = link.attrs['href']
            outer_link.append(temp)
        return outer_link

    # 获取一个讨论组里所有的发言（discussion）
    def get_forum_data(self, url):
        forum = []
        page_html = self.moodle.session.get(url).text
        bsObj = BeautifulSoup(page_html, 'lxml')
        forum_data = bsObj.findAll("tr", attrs={'class': 'discussion subscribed'})
        for link in forum_data:
            temp = {}
            data = link.find("th", attrs={'scope': 'row'}).div.a
            temp['discuss_title'] = data.attrs['title']
            temp['discuss_url'] = data.attrs['href']
            temp['discuss_start_time'] = \
                link.find("td", attrs={'class': 'author align-middle fit-content limit-width px-3'}).div.find("div",
                                                                                                              attrs={
                                                                                                                  'class': 'author-info align-middle'}).findAll(
                    "div", attrs={'class': 'line-height-3'}, )[1].time.attrs[
                    'data-timestamp']

            temp['discuss_last_post_time'] = \
                link.find("td", attrs={'class': 'text-left align-middle fit-content limit-width px-3'}).div.find("div",
                                                                                                                 attrs={
                                                                                                                     'class': 'author-info align-middle'}).findAll(
                    "div", attrs={'class': 'line-height-3'}, )[1].a.time.attrs[
                    'data-timestamp']
            forum.append(temp)
        return forum

    # Warning： 在 set_current_page() 后运行
    # 获取网页中所有讨论组，储存讨论组名字和链接，并调用 get_forum_data， 将返回值储存
    def get_forum(self):
        forum = []
        bsObj = self.__bsObj
        forum_link = bsObj.find("ul", attrs={'class': 'topics'}).findAll("a", href=re.compile(".*((/mod/)(forum))"))
        print("There are " + str(len(forum_link)) + " forum in this web")
        for link in forum_link:
            if 'href' in link.attrs:
                if 'instancename' in link.span.attrs['class']:
                    temp = {}
                    temp['forum_name'] = link.span.text
                    temp['forum_url'] = link.attrs['href']
                    temp['forum_data'] = self.get_forum_data(temp['forum_url'])
                    forum.append(temp)
        return forum

    # 从Moodle界面获得全部课程
    def getList(self, all):

        # all == true 获取所有课程
        # all == false 获取started课程
        if all:
            courseListJson = url_and_json_info.all_course_list_json
        elif not all:
            courseListJson = url_and_json_info.stared_course_list_json
        else:
            courseListJson = url_and_json_info.all_course_list_json

        # json的地址分两部分，一部分的sesskey需要先获取再打印，另一部分的info是固定的
        jsonRqtUrl = url_and_json_info.course_list_request_url_1 + self.moodle.sesskey + url_and_json_info.course_list_request_url_2

        # 请求课程列表的json
        courseJson = self.moodle.session.post(jsonRqtUrl, json=courseListJson)
        if courseJson.status_code == 200:
            # 200 提交成功
            rep = courseJson.json()
            # 清洗数据
            return self.__data_cleanse(rep)
        return False

    # private 方法， 用于清洗json数据（仅可以被getList方法调用）
    def __data_cleanse(self, courseJson):
        list_data = []
        # json 就是套娃，大套娃套小套娃，按照名字依次打开套娃，获得需要的数据
        courseJson = courseJson[0]['data']['courses']
        for i in range(len(courseJson)):
            temp = {}
            temp['course_name'] = courseJson[i]['fullname']
            temp['course_url'] = courseJson[i]['viewurl']
            list_data.append(temp)
        return list_data

if __name__ == '__main__':
    # 样例输入
    # 创建Moodle对象，并实例化
    moodle = Moodle()
    # 用账号和密码模拟登录
    print(moodle.login("scyzz5", "Lxygwqfqsgct1s-"))
    # 创建MooldeCrawler对象，并实例化
    Crawler = MoodleCrawler(moodle)
    # 获取部分（started）课程
    print(Crawler.getList(False))
    # 设置监视目标未ACE课程
    Crawler.set_current_page("https://moodle.nottingham.ac.uk/course/view.php?id=104761")
    # 获取ACE课程中全部文件夹
    print(Crawler.get_folder())
    # 获取ACE课程中全部内部链接
    print(Crawler.get_inner_link())
    # 获取ACE课程中全部外部链接
    print(Crawler.get_outer_link())
    # 获取ACE课程中全部讨论组和每个讨论组的内容
    print(Crawler.get_forum())
