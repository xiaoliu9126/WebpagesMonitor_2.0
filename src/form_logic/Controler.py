from src.form_logic.Moodle import Moodle
from src.form_logic.MoodleCrawler import MoodleCrawler
from src.form_logic.File import File

class Controler():
    # 测试开关
    test = True
    # 用于登录的对象 Moodle
    moodle = None
    # 用于爬取信息的对象 Moodle_crawler
    moodle_crawler = None
    # 用于处理本地文件的对象 File
    file = None
    # 是否保存用户名和密码
    if_save_username_and_password = False
    # 所有被扫描的课程中，全部的更新内容
    user_data_update = []
    # 储存被忽略的讨论组的话题
    __forum_ignore_list = {}
    # 储存账号和密码
    __passData = None

    def __init__(self):
        self.moodle = Moodle()
        self.moodle_crawler = MoodleCrawler(self.moodle)
        self.file = File()

    def login(self, username, password, save):
        if_success = self.moodle.login(username, password)
        if if_success is False:
            return False
        self.__passData = self.moodle.passData
        self.if_save_username_and_password = save
        self.save_user_data()
        return if_success

    # 扫描所有被监控课程，对比本地，返回更新
    def scanning(self):
        # 初始化更新总更新信息
        self.user_data_update = []

        past_courses_info = self.file.loadJson(self.file.user_info_absolute_path +
                                               self.__passData['username'] + "_course")
        user_info = self.show_all_courses()
        current_course_info = []
        if not past_courses_info:
            past_courses_info = []

        for i in range(len(user_info)):
            if user_info[i]['monitoring']:
                course_name = user_info[i]['course_name']

                past_course_info = {}

                for j in range(len(past_courses_info)):
                    if range(len(past_courses_info)) == 0:
                        break
                    if past_courses_info[j].get('Name') == course_name:
                        past_course_info = past_courses_info[j]
                        break
                current_course_info.append(self.course_compare(past_course_info, user_info[i]['course_name'], user_info[i]['course_url']))

        print(self.user_data_update)
        self.file.saveJson(self.file.user_info_path, current_course_info, self.__passData['username'] + "_course")
        return self.user_data_update

    # 扫码某一课程，返回课程内的全部信息
    def scan_course(self, course_name, url):
        print("现在开始扫描课程：" + course_name)
        self.moodle_crawler.set_current_page(url)
        folder = self.moodle_crawler.get_folder()
        inner_link = self.moodle_crawler.get_inner_link()
        outer_link = self.moodle_crawler.get_outer_link()
        forum = self.moodle_crawler.get_forum()

        course_info = {'Name': course_name, 'url': url, 'folder': folder, 'inner_link': inner_link,
                       'outer_link': outer_link, 'forum': forum}

        return course_info

    # 将某一课程重新扫描并与本地对比，返回更新信息
    def course_compare(self, past_course_info, course_name, url):

        current_course_info = self.scan_course(course_name, url)

        if not current_course_info:
            return False

        folder_update = self.compare_list(past_course_info.get('folder'), current_course_info['folder'])
        inner_link_update = self.compare_list(past_course_info.get('inner_link'), current_course_info['inner_link'])
        outer_link_update = self.compare_list(past_course_info.get('outer_link'), current_course_info['outer_link'])
        forum_update = self.compare_forum(past_course_info.get('forum'), current_course_info['forum'])

        # 课程更新
        course_update = {'Name': course_name, 'url': url, 'folder': folder_update, 'inner_link': inner_link_update,
                         'outer_link': outer_link_update, 'forum': forum_update}

        # 将更新内容添加到更新列表
        self.user_data_update.append(course_update)
        # 返回更新后的课程信息
        return current_course_info

    # 对list进行对比
    def compare_list(self, past_course_list, current_course_list):
        list_update = []

        if past_course_list is None:
            return current_course_list

        for element in current_course_list:
            if element not in past_course_list:
                if element not in list_update:
                    list_update.append(element)
        return list_update

    # 对forum进行对比
    def compare_forum(self, past_course_forum, current_course_forum):
        forum_update = []
        if past_course_forum is None:
            return current_course_forum
        for current_forum in current_course_forum:
            flag = False
            for past_forum in past_course_forum:
                if current_forum['forum_url'] == past_forum['forum_url']:
                    flag = True
                    break
            if flag is False:
                forum_update.append(current_forum)

        for current_forum in current_course_forum:
            flag = False
            forum_discuss_update = {}
            for past_forum in past_course_forum:
                if current_forum['forum_url'] == past_forum['forum_url']:
                    forum_discuss_update['forum_name'] = current_forum['forum_name']
                    forum_discuss_update['forum_url'] = current_forum['forum_url']
                    forum_discuss_update['forum_data'] = []
                    for discuss in current_forum['forum_data']:
                        if discuss not in past_forum['forum_data']:
                            if current_forum['forum_url'] in self.__forum_ignore_list and \
                                    discuss['discuss_url'] in self.__forum_ignore_list.get(
                                current_forum['forum_url']):
                                continue

                            flag = True
                            forum_discuss_update['forum_data'].append(discuss)
            if flag:
                forum_update.append(forum_discuss_update)
        # https://www.bejson.com/jsonviewernew/
        return forum_update

    # 更新课程列表，增添或删除课程后使用
    def update_course_list(self):
        new_list = self.moodle_crawler.getList(True)
        for i in range(len(new_list)):
            new_list[i]['monitoring'] = False
            new_list[i]['id'] = i
        self.file.saveJson(self.file.user_info_path, new_list, self.__passData['username'] + "_courseList")
        return new_list

    # 打印并返回所有课程
    def show_all_courses(self):
        course_list = self.file.loadJson(self.file.user_info_absolute_path +
                                              self.__passData['username'] + "_courseList")
        if not course_list:
            course_list = self.update_course_list()

        # 打印所有课程
        if self.test:
            for i in range(len(course_list)):
                print(course_list[i]['id'])
                print(course_list[i]['course_name'])
                print(course_list[i]['course_url'])
                print(course_list[i]['monitoring'])

        return course_list

    # 增加被监控的课程，返回全部课程信息
    def add_new_monitoring_course(self, courses_id):
        old_list = self.file.loadJson(self.file.user_info_absolute_path +
                                              self.__passData['username'] + "_courseList")
        for course_id in courses_id:
            old_list[int(course_id)]['monitoring'] = True

        course_list = old_list
        self.file.saveJson(self.file.user_info_path, course_list, self.__passData['username'] + "_courseList")
        return course_list

    # 删除被监控的课程，返回全部课程信息
    def delete_monitoring_course(self, courses_id):
        old_list = self.file.loadJson(self.file.user_info_absolute_path +
                                      self.__passData['username'] + "_courseList")
        if not old_list:
            return

        for course_id in courses_id:
            old_list[int(course_id)]['monitoring'] = False

        course_list = old_list
        self.file.saveJson(self.file.user_info_path, course_list, self.__passData['username'] + "_courseList")
        return course_list

    # 打印被监控的课程
    def show_monitoring_course(self):
        course_list = self.file.loadJson(self.file.user_info_absolute_path +
                                      self.__passData['username'] + "_courseList")

        # 异常情况：找不到文件
        if not course_list:
            return False

        # 打印所有被监控的课程
        monitoring_course_list = []
        for course_id in range(len(course_list)):
            if course_list[int(course_id)]['monitoring']:
                print(course_list[int(course_id)]['course_name'])
                monitoring_course_list.append(course_list[int(course_id)]['id'])

        return monitoring_course_list

    def forum_ignore(self, forum_url, discuss_url):
        forum_ignore_list = self.file.loadJson(self.file.user_info_absolute_path +
                                      self.__passData['username'] + "_ignoreList")

        if forum_ignore_list:
            self.__forum_ignore_list = forum_ignore_list
        if self.__forum_ignore_list.get(forum_url) is None:
            self.__forum_ignore_list[forum_url] = []
        if discuss_url not in self.__forum_ignore_list.get(forum_url):
            self.__forum_ignore_list[forum_url].append(discuss_url)

        self.file.saveJson(self.file.user_info_path, self.__forum_ignore_list,
                                        self.__passData['username'] + "_ignoreList")

    def remove_forum_ignore(self, forum_url, discuss_url):
        self.__forum_ignore_list = self.file.loadJson(self.file.user_info_absolute_path +
                                                      self.__passData['username'] + "_ignoreList")

        if not self.__forum_ignore_list:
            self.__forum_ignore_list[forum_url] = []

        if self.__forum_ignore_list.get(forum_url) is None:
            self.__forum_ignore_list[forum_url] = []

        self.__forum_ignore_list = {}

        for key in self.__forum_ignore_list.keys():
            if key == forum_url:
                value = self.__forum_ignore_list.get(key)
                if discuss_url in value:
                    value.remove(discuss_url)
                    self.__forum_ignore_list[key] = value
                    break

        self.file.saveJson(self.file.user_info_path, self.__forum_ignore_list,
                           self.__passData['username'] + "_ignoreList")

    def show_ignore(self):
        return self.__forum_ignore_list

    def re_login(self):
        return self.moodle.re_login()

    def log_out(self):
        return self.moodle.log_out()

    def test_connect(self):
        return self.moodle.test_connect()

    def save_user_data(self):
        user_info = {'username': self.__passData['username']}
        if self.if_save_username_and_password is False:
            user_info['password'] = ''
        else:
            user_info['password'] = self.__passData['password']
        user_info['logintoken'] = ''
        user_info['anchor'] = ''
        self.file.saveJson(self.file.user_info_path, user_info, user_info['username'])


if __name__ == '__main__':
    controler = Controler()
    # 登录
    print(controler.login("scyzz5", "Lxygwqfqsgct1s-", True))
    # 打印全部课程
    controler.show_all_courses()
    # 选择监控的课程
    controler.add_new_monitoring_course([1])
    controler.add_new_monitoring_course([17])
    controler.add_new_monitoring_course([11])
    controler.add_new_monitoring_course([22])
    controler.add_new_monitoring_course([0])

    # controler.add_new_monitoring_course([15])
    # 移除被监控的课程
    controler.delete_monitoring_course([4])
    controler.delete_monitoring_course([5])
    # 打印所有被监控的课程
    print(controler.show_monitoring_course())
    # 扫描所有被监控的课程
    # controler.scanning()
    # # 忽略某一讨论组中的某一话题
    # controler.forum_ignore('https://moodle.nottingham.ac.uk/mod/forum/view.php?id=4251308',
    #                        'https://moodle.nottingham.ac.uk/mod/forum/discuss.php?d=575933')
    # # 打印所有被忽略的话题
    # print(controler.show_ignore())
    # # 移除某一个被忽略的话题
    # controler.remove_forum_ignore('https://moodle.nottingham.ac.uk/mod/forum/view.php?id=4251308',
    #                        'https://moodle.nottingham.ac.uk/mod/forum/discuss.php?d=575933')
    # print(controler.show_ignore())