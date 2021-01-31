import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from class_define import Email
import accounts

# 实例化一个email，并设置发送邮箱，邮箱密码，接收邮箱
email = Email(accounts.sender_email, accounts.sender_pwd, accounts.receiver_email)


# 定义发送邮件函数
def send(content):
    try:
        # 连接163邮箱的服务器并登录邮箱
        con = smtplib.SMTP_SSL('smtp.163.com', 465)
        con.login(email.mail_uid, email.mail_pwd)

        # 创建邮件对象
        msg = MIMEMultipart()

        # 设置邮件主题、发件人、收件人、邮件内容
        msg['Subject'] = Header('找回密码', 'utf-8').encode()
        msg['From'] = email.mail_from
        msg['To'] = email.mail_to
        text = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text)

        # 发送邮件后退出邮箱
        con.sendmail(email.mail_from, email.mail_to, msg.as_string())
        con.quit()

        print("提醒邮件发送成功！")

    except smtplib.SMTPException as e:
        print('提醒邮件发送失败！error：', e)

# send("今日打卡已完成！")
