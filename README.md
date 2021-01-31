# 郑州大学师生健康状况上报平台自动打卡



## 项目简介

自2020年初新冠疫情以来，全国各高校大多数要求实现师生健康状况每日上报，该项目是个人练习作品，旨在实现`郑州大学健康状况上报平台`的自动打卡。可以基本完成以下功能：

1. 运行程序后自动打卡
2. 将每次的打卡结果（无论成功与否）通过邮件发送给用户



## 环境&软件

```
1. Python (version: 3.8.3)
2. selenium
3. smtplib
4. Google Chorme 浏览器 (version: 88.0.4324.104（正式版本 64 位）)
5. Chormedirver (version: 88.0.4324.96)

注：Chromedriver需要与Chrome浏览器版本一致
```



## 实现思路

#### step 1. 分析健康打卡的流程（系统分析）

`郑州大学健康状况上报平台`的每日健康打卡主要涉及三个页面和/或流程：

**1. 登录页：** 用户输入账号密码并点击登录，从而进入状态页

**2. 状态页：** 显示用户今日的打卡状态，可通过该页面的`本人填报`按钮进入下一个页面

**3. 打卡页：** 通过表单填写当日的健康状况，然后提交表单，完成打卡



#### step 2. 初步确定功能和需求（系统设计）

**1. 自动打卡：** 希望通过运行一段程序脚本，实现自动登录打卡系统，并完成当日的健康打卡。查阅资料发现，`selenium`可以实现模拟浏览器中的操作。`Chromedriver`是Chrome浏览器的驱动程序，安装后就能让`selenium`启动Chrome浏览器了。

**2. 即时反馈：** 是否打卡成功？给用户以反馈。这可以通过发送邮件实现。查阅资料发现，Python可以通过`smtplib`发送邮件，提前准备一个用于发送邮件的邮箱和密码即可。



#### step 3. 实现规划的具体功能（系统实施）

主要分为四个文件，分别用于定义类 `class_define.py`、设置账号密码等私人信息 `accounts.py`、自动打卡`main.py`、发送提醒邮件`send_email.py`



`class_define.py` 定义了**(1) 用户类** 和 **(2) 邮箱类**

```python
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
```



`accounts.py`  **这个文件需要修改为自己的账号密码**

```python
# （1）设置登陆打卡系统的账号和密码
daka_uid = '201*********'   # 学号
daka_pwd = '********'       # 密码（默认身份证后八位）

# （2）设置发送邮件的邮箱账号和密码（目前仅支持163邮箱）
sender_email = 'example@163.com'     # 邮箱账号
sender_pwd = '********'              # 邮箱密码

# （3）设置接收提醒消息的邮箱（仅测试过用qq邮箱接收消息）
receiver_email = 'example@qq.com'
```



`main.py`  利用`selenium`和`Chromedriver`实现模拟浏览器完成自动打卡

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from class_define import User
import send_email
import accounts

# 实例化一个user，并定义用户名和密码
user = User(accounts.daka_uid, accounts.daka_pwd)

# 设置不显示浏览器窗口
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

# 打开健康打卡系统页面
browser = webdriver.Chrome(options=chrome_options)
print("正在打开zzu打卡系统...")
# browser = webdriver.Chrome()
browser.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")
print("zzu打卡系统已开启，正在填写账号密码...")

try:

    # 填写用户名和密码并登陆
    browser.find_element_by_name("uid").send_keys(user.uid)
    browser.find_element_by_name("upw").send_keys(user.pwd)
    browser.find_element_by_name("smbtn").click()
    print("登录成功！")

    # 切换到iframe页面
    browser.implicitly_wait(10)
    iframe = browser.find_element_by_tag_name("iframe")
    browser.switch_to.frame(iframe)

    # 检查是否已经打卡
    browser.find_element_by_xpath('//*[@id="bak_0"]/div[7]/span')
    msg = browser.find_element_by_xpath("//*[@id='bak_0']/div[7]/span").text
    print('学号为' + user.uid + "的用户：" + msg)
    global email_message
    if msg == "今日您已经填报过了":
        # 如果已经打卡则返回msg
        email_message = msg
    else:
        # 如果未打卡则执行打卡操作
        browser.find_element_by_xpath('//*[@id="bak_0"]/div[13]/div[5]/div[4]/span').click()
        # 跳转到提交页面并点击打卡按钮
        browser.find_element_by_xpath('//*[@id="bak_0"]/div[7]/div[2]/div[2]/div[6]/div[4]').click()
        email_message = "今日自动打卡成功！"

except Exception as err:
    print("发生错误，打卡失败：\n" + str(err))
    email_message = "发生错误，打卡失败：\n" + str(err)

finally:
    browser.quit()
    send_email.send(email_message)

```



`send_email.py`  利用`smtplib`实现了发送邮件功能

```python
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

```



#### step 4. 运行脚本以自动打卡（系统运行）

在`accounts.py`中设置好账号密码等信息后，运行`main.py`。看见控制台中输出以下内容：

```
正在打开zzu打卡系统...
zzu打卡系统已开启，正在填写账号密码...
登录成功！
学号为201*********的用户：今日您已经填报过了
提醒邮件发送成功！

进程已结束,退出代码0
```

同时，事先定义的邮箱收到了反馈的邮件，内容为：`"今日自动打卡成功！"`。

至此，两个功能已经基本实现。



## 不足之处

1. 目前还需手动执行项目，后期可以考虑实现**定时打卡**的功能，例如每天 00:10 打卡，以实现真正意义上的自动打卡。
2. 由于邮箱系统的限制，给用户发送的提醒邮件主题只能设置为`“找回密码”`，否则发送无法完成。后续将继续探索Python实现邮件发送的其他项目，找到合适的解决办法。
3. 打卡只能单用户进行，后续继续考虑实现**多用户打卡**的功能实现。



## 参考资料

1. 使用Python实现平台自动打卡  https://mtics.top/auto-sign-zzu-jksb/

2. Selenium自动疫情填报  https://zhuanlan.zhihu.com/p/112343025

3. Python通过smtplib发送邮件(2020最新最全版)  https://blog.csdn.net/yuting209/article/details/105424833