# 定义用户类
class User:
    uid = ""
    pwd = ""

    def __init__(self, uid, pwd):
        self.uid = uid
        self.pwd = pwd


# 定义邮件类
class Email:
    mail_uid = ""
    mail_pwd = ""
    mail_from = ""
    mail_to = ""

    def __init__(self, mail_uid, mail_pwd, mail_to):
        self.mail_uid = mail_uid
        self.mail_pwd = mail_pwd
        self.mail_from = str(self.mail_uid) + " <" + str(self.mail_uid) + ">"
        self.mail_to = mail_to
