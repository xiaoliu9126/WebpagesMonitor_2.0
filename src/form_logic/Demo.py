# 定义一种Json类型存储用户数据

# UserData:
#     login:
#         username = scyxxx
#         password = sjdlfkjdssdf02Q
#         sesskey = ''
#     data[
#         course
#             Fullnema: COMP2043 XXXXXXXXXXXXXX
#             Link: 'moodle.nottingham.edu.cn/XXX/XXXXX/XXXXXXXXXXX'
#             file:
#                 [File1:
#                     loaded = False
#                     path = C:/UserData/scyxxx
#                     Data = 2020/11/11
#                     Link = /mod/103423/XXXXXXXXX
#
#
#                 ]
#             Folder:
#                 [Folder1:
#                     loaded = False
#                     path = C: / UserData / scyxxx
#                     Data = 2020 / 11 / 11
#                     Link = / mod / 103423 / XXXXXXXXX
#
#                 ]
#             Form:
#                 [Form1
#                     link = ""
#                     Data = 2020/11/11
#                     Name = ""
#                 ]
#             Url:
#                 [Url1:
#                     link = ""
#                     Data = 2020/11/11
#                     Name = ""
#
#                 ]
#          ]


User_data = {'Login': {'username': '', 'password': '', 'anchor': '', 'logintoken': ''},
             'data': {'courses': []}
             }
File = {'loaded': False, 'filePath': '', 'date': '', 'link': '', 'name': ''}
Folder = {'loaded': False, 'filePath': '', 'date': '', 'link': '', 'name': ''}
Form = {'date': '', 'link': '', 'name': ''}
Url = {'date': '', 'link': '', 'name': ''}

course = {'fullname': '', 'link': '', 'File': [], 'Folder': [], 'Form': [], 'Url': []}



def login():
    # import Moodle

    return


if __name__ == '__main__':
    print("0")
