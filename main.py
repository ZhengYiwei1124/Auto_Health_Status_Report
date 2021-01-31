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