
import os
import json

class File():
    #   If 'UserInfo' and 'UserFiles' two files not exist
    #   then build these two files
    user_files_absolute_path = None
    user_info_absolute_path = None
    user_files_path = None
    user_info_path = None

    def __init__(self):
        try:
            userInfo = "\\UserInfo\\"
            userFiles = "\\UserFiles\\"
            self.user_files_absolute_path = self.isFileExists(userFiles)
            self.user_info_absolute_path = self.isFileExists(userInfo)
            self.user_info_path = userInfo
            self.user_files_path = userFiles
        except:
            return False


    #   input: relative path Exp: "\\UserInfo\\scyzz5\\"
    #   output: absolute path (if not exist, build it)
    def isFileExists(self, path):
        try:
            nowPath = os.getcwd()
            Path = nowPath + path

            isExists = os.path.exists(Path)
            if not isExists:
                os.makedirs(Path)
            return Path
        except:
            return False


    #   input: Json file's absolute path
    #   output: data in Json
    def loadJson(self, Path):
        try:
            with open(Path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except:
            return False


    #   isFileExists("\\UserFiles\\scyzz5\\Helloword\\")


    #   input: relative path, data and name
    #   output: absolute path (if not exist, build it)
    def saveJson(self, Path, data, name):
        try:
            if self.isFileExists(Path) is False:
                return False
            else:
                with open(self.isFileExists(Path) + name, 'w', encoding='utf-8') as f:
                    json.dump(data, f)
                    return True
        except:
            return False


if __name__ == '__main__':
    a = 'a'

# data = {"Url": True}
# saveJson("\\UserInfo\\", data, "SchoolUrl.json")


# 下载文件
# def downloadFileByUrl(session, sesskey, url):
#     reqUrl = "https://moodle.nottingham.ac.uk/mod/folder/download_folder.php"
#     downloadForm = {}
#     downloadForm['sesskey'] = sesskey
#     downloadForm['id'] = url[str(url).find("id=") + 3: str(url).find("id=") + 10]
#     print(downloadForm)
#
#     File = session.post(reqUrl, data=downloadForm, stream=True)
#
#     import os.path
#
#     from sys import stdout
#     print(File.headers)
#     filename = File.headers["Content-Disposition"]
#     filename = filename[filename.find("\"") + 1: len(filename) - 1]
#     print(filename)
#     filesize = File.headers["Content-Length"]
#
#     file_to_save = os.path.join(os.getcwd(), filename)  # 获取当前路径
#     print(file_to_save)  # 下载的本地路径
#
#     with open(file_to_save, "wb") as f:
#         # f.write(File.content)
#         chunk_size = 1280
#         times = int(filesize)
#         print("begin download")
#         import time
#         time1 = time.time()
#         for chunk in File.iter_content(chunk_size):
#             f.write(chunk)
#         print(time.time() - time1)
#         import zipfile
#         # import Demo
#         # Demo.isFileExists(filename[0:len(filename-4)])
#
#     return
