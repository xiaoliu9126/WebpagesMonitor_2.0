#   本文件存在的意义：
#   本文将包括了全部对Moodle进行处理的方法包括：连接Moodle， 搜索Moodle， 等等

import requests
from bs4 import BeautifulSoup

import re
import json
import os
from util.common_util import *

def newCnt(username, password):
    passData = {}
    passData["username"] = username
    passData["password"] = password
    passData["anchor"] = ""
    passData["logintoken"] = ""
    login_url = "https://moodle.nottingham.ac.uk/login/index.php"
    # 建立session对象并且访问login
    session = requests.session()
    login_html = session.get(login_url)
    try:
        # 获取网页全部信息，查询token 将值放入passData
        soup = BeautifulSoup(login_html.text, 'lxml')
        login_token_mess = soup.find(attrs={'name':'logintoken'})
        login_token_value = login_token_mess.attrs['value']
        passData["logintoken"] = login_token_value
    except:
        print("Error: moodle spider get session error")
        return

    # 将获取的登陆信息传递给session服务器
    login_OK = session.post(login_url, data=passData)
    return session



# 从Moodle界面获得全部课程
# def getList(session):
#     HomeUrl = "https://moodle.nottingham.ac.uk/my/"
#
#     # 请求打印全部课程的json
#     courseListJson = [{"index": 0, "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
#                        "args": {"offset": 0, "limit": 0, "classification": "all", "sort": "fullname", "customfieldname": "", "customfieldvalue": ""}}]
#
#     # json的地址分两部分，一部分的sesskey需要先获取再打印，另一部分的info是固定的
#     jsonRqtUrl_1 = "https://moodle.nottingham.ac.uk/lib/ajax/service.php?sesskey="
#     jsonRqtUrl_2 = "&info=core_course_get_enrolled_courses_by_timeline_classification"
#
#
#     # 通过搜索获取sesskey 速度欠佳，可以靠beautifulsoup改进，后续完善
#     homepage = session.get(HomeUrl)
#     homepage_text = homepage.text
#     sekey = str(homepage_text).find("sesskey")
#     sesskey = homepage_text[sekey + 10:sekey + 20]
#     jsonRqtUrl = jsonRqtUrl_1 + sesskey + jsonRqtUrl_2
#
#     # 请求课程列表的json
#     courseJson = session.post(jsonRqtUrl, json=courseListJson)
#     if courseJson.status_code == 200:
#         rep = courseJson.json()
#
#     print(rep) #查看清洗前的数据
#
#     # 清洗数据
#     courselist = dataCleanse(rep)
#     return courselist

def getList(session):
    HomeUrl = "https://moodle.nottingham.ac.uk/my/"
    # 请求打印全部课程的json
    courseListJson = [{"index": 0, "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
                       "args": {"offset": 0, "limit": 0, "classification": "all", "sort": "fullname", "customfieldname": "", "customfieldvalue": ""}}]

    # json的地址分两部分，一部分的sesskey需要先获取再打印，另一部分的info是固定的
    jsonRqtUrl_1 = "https://moodle.nottingham.ac.uk/lib/ajax/service.php?sesskey="
    jsonRqtUrl_2 = "&info=core_course_get_enrolled_courses_by_timeline_classification"

    # 通过搜索获取sesskey 速度欠佳，可以靠beautifulsoup改进
    homepage = session.get(HomeUrl)
    homepage_soup = BeautifulSoup(homepage.text, 'lxml')
    homepage_soup_sesskey = homepage_soup.find('a',attrs={'data-title':'logout,moodle'})
    homepage_soup_sesskey_url = homepage_soup_sesskey.attrs['href']
    sekey = str(homepage_soup_sesskey_url).find("sesskey=")
    sesskey = str(homepage_soup_sesskey_url)[sekey + 8:sekey + 18]
    jsonRqtUrl = jsonRqtUrl_1 + sesskey + jsonRqtUrl_2
    # 请求课程列表的json
    courseJson = session.post(jsonRqtUrl, json=courseListJson)
    if courseJson.status_code == 200:
        rep = courseJson.json()
    # 清洗数据
    coursedata = dataCleanse(rep)
    # coursedatajson = json.dumps(coursedata)
    return coursedata


def dataCleanse(courseJson):
    # json 就是套娃，大套娃套小套娃，按照名字依次打开套娃，获得需要的数据
    courseJson = courseJson[0]['data']['courses']
    courseitem_list = []
    for i in range(len(courseJson)):
        courseName = courseJson[i]['fullname']
        courseUrl = courseJson[i]['viewurl']
        courseitem_list.append({"courseName": courseName, "courseUrl": courseUrl})
    return courseitem_list


# 下载课件到指定文件夹
def urlAnalysis(session, name, html):
    # 新建课程文件夹用来存储pdf
    # TODO 该位置需要修改
    os.chdir("E:\python_code\WebpagesMonitor_2.0\src\coursedata")
    print(os.getcwd())
    print("__________")
    if not os.path.exists(name):
        os.makedirs(name)
    os.chdir(os.path.join(os.getcwd(), name))
    file_list = os.listdir(os.path.join(os.getcwd()))
    # 获取网站
    folder_html = session.get(html)
    Folder = {}
    folder_soup = BeautifulSoup(folder_html.text, 'lxml')
    folderUrl = folder_soup.findAll("a", href=re.compile(".*((/mod/)(folder))"))
    print("There are " + str(len(folderUrl)) + " Folder in this web")
    # 下载网址
    for link in folderUrl:
        if 'href' in link.attrs:
            if 'instancename' in link.span.attrs['class']:
                Folder[link.span.text] = link.attrs['href']
                # 下载pdf
                pdf_down_html = session.get(link.attrs['href'])
                pdf_down_soup = BeautifulSoup(pdf_down_html.text, 'lxml')
                pdf_down_url = pdf_down_soup.findAll("a", href=re.compile(".*(mod_folder)"))
                for link in pdf_down_url:
                    if 'href' in link.attrs:
                        if link.text not in file_list:
                            print("download")
                            print(link.text)
                            pdf_down = session.get(link.attrs['href'], stream="TRUE")
                            with open(link.text, "wb") as Pypdf:
                                for chunk in pdf_down.iter_content(chunk_size=1024):  # 1024 bytes
                                    if chunk:
                                        Pypdf.write(chunk)
                        else:
                            print("file is exist")
                    else:
                        print("nothing to down")
    return Folder

# 下载课程公告到文件夹中
def downAnnouncements(session, username, name, html):
    # 获取网站
    folder_html = session.get(html)
    folder_soup = BeautifulSoup(folder_html.text, 'lxml')
    folderUrl = folder_soup.findAll("a", href=re.compile(".*((/mod/)(forum))"))
    # 下载网址
    announce_mess = []
    for link in folderUrl:
        # if 'href' in link.attrs and link.text=='Announcements Forum':
        if 'href' in link.attrs and link.text =='Announcements Forum':      # .lower().find('announcements'):
            # 下载公告信息到课程文件夹
            Announce_down_html = session.get(link.attrs['href'])
            Announce_down_soup = BeautifulSoup(Announce_down_html.text, 'lxml')
            Announce_down_url = Announce_down_soup.findAll("a", href=re.compile(".*((/mod/)(forum/)(discuss.php.*))"))
            for announce in Announce_down_url:
                if 'aria-label' in announce.attrs:
                    last_Announce_down_html = session.get(announce.attrs['href'])
                    last_Announce_down_soup = BeautifulSoup(last_Announce_down_html.text, 'lxml')
                    # 我们获得该课程的公告的信息
                    subject = last_Announce_down_soup.find("h3", attrs={'data-region-content':'forum-post-core-subject'}).text
                    time = last_Announce_down_soup.find("time").text
                    context = last_Announce_down_soup.find('div', {'class': 'post-content-container'}).text
                    announce_dict = {'subject':subject,'time':time,'context':context}
                    announce_mess.append(announce_dict)
    # 将announce_mess 存储到指定文件夹 可以用数据库进行改进
    # 文件名字
    announcefilename = name + 'file.json'
    user_announcement_folder = os.path.join(USER_ALL_COURSE, 'data', username, "Announcement")
    if os.path.exists(user_announcement_folder):
        user_announcement_path = os.path.join(user_announcement_folder, announcefilename)
    else:
        os.makedirs(user_announcement_folder)
        user_announcement_path = os.path.join(user_announcement_folder, announcefilename)

    with open(user_announcement_path, mode='w', encoding='utf-8') as file:
        json.dump(announce_mess, file, ensure_ascii=False)
        file.close()

    return announcefilename

# 下载课程公告到文件夹中
def downForum(session, username, name, html):
    # 获取网站
    folder_html = session.get(html)
    folder_soup = BeautifulSoup(folder_html.text, 'lxml')
    folderUrl = folder_soup.findAll("a", href=re.compile(".*((/mod/)(forum))"))
    # 下载网址
    announce_mess = []
    for link in folderUrl:
        if 'href' in link.attrs and link.text.lower().find('forum') and link.text != 'Announcements Forum':
            # 下载公告信息到课程文件夹
            Announce_down_html = session.get(link.attrs['href'])
            Announce_down_soup = BeautifulSoup(Announce_down_html.text, 'lxml')
            Announce_down_url = Announce_down_soup.findAll("a", href=re.compile(".*((/mod/)(forum/)(discuss.php.*))"))
            for announce in Announce_down_url:
                if 'aria-label' in announce.attrs:
                    last_Announce_down_html = session.get(announce.attrs['href'])
                    last_Announce_down_soup = BeautifulSoup(last_Announce_down_html.text, 'lxml')
                    # 我们获得该课程的公告的信息
                    subject = last_Announce_down_soup.find("h3", {'class': 'discussionname'}).text
                    time = last_Announce_down_soup.find("time").text
                    context = last_Announce_down_soup.find('div', {'class': 'post-content-container'}).text
                    announce_dict = {'subject':subject,'time':time,'context':context}
                    announce_mess.append(announce_dict)
    # 将announce_mess 存储到指定文件夹 可以用数据库进行改进
    # 文件名字
    forumfilename = name + 'file.json'
    user_announcement_folder = os.path.join(USER_ALL_COURSE, 'data', username, "Forum")
    if os.path.exists(user_announcement_folder):
        user_announcement_path = os.path.join(user_announcement_folder, forumfilename)
    else:
        os.makedirs(user_announcement_folder)
        user_announcement_path = os.path.join(user_announcement_folder, forumfilename)

    with open(user_announcement_path, mode='w', encoding='utf-8') as file:
        json.dump(announce_mess, file, ensure_ascii=False)
        file.close()

    return forumfilename

if __name__ == '__main__':
    # "username" = "scyzz5"
    # "password" = "Lxygwqfqsgct1s-"

    # scyjw3

    # Wlwyhwjy199761&0827

    session = newCnt("scyjw3" , "Wlwyhwjy199761&0827")
    # getList(session)
    # folder = urlAnalysis(session, "test", "https://moodle.nottingham.ac.uk/course/view.php?id=10822")
    # getList(session)
    # downloadsCoursepdf(session)
    # folder = urlAnalysis(session,"input heml")
    # downloadsCoursepdf(session, folder)
    # downAnnouncements(session, "ACE (1010) wd", "https://moodle.nottingham.ac.uk/course/view.php?id=104761")
    # downForum()
