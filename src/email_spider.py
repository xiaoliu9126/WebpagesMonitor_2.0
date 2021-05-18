# -*- coding: utf-8 -*-
# zmail库：可以用几行代码帮我们收取一封邮件
# import zmail
#建立一个email的连接
def newEmail(username,password):
    # test for qq 邮箱
    # 输入你的邮箱和授权码+
    # 如何获得授权码https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256
    username = 'xiao.l.9126@qq.com'
    password = 'aximaarwckdvdjee'
    # username = 'mailteam@qq.com'
    # password = 'gzoyimtltnqsbdba'
    server = zmail.server(username,password)
    return server

if __name__ == "__main__":
    # 输入账号和密码
    server = newEmail("","")
    # 获取最新的一封邮件
    mails = server.get_mails()
    print(mails)
    # mail=server.get_mail(1)
    # 读取邮件
    for mail in mails:
        print(mail['id'])
        print(mail['subject'])
        print(mail['from'])
        print(mail['content_text'])

