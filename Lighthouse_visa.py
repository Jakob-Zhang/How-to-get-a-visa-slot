from bs4 import BeautifulSoup
import time
from selenium import webdriver

month_dic = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

#def send_email(subject):
    # from smtplib import SMTP_SSL
    # from email.mime.text import MIMEText
    # from email.header import Header
    # email_from = ""  # 改为自己的发送邮箱
    # email_to = ""  # 接收邮箱
    # hostname = "smtp.qq.com"  # 不变，QQ邮箱的smtp服务器地址
    # login = ""  # 发送邮箱的用户名
    # password = ""  # 发送邮箱的密码，即开启smtp服务得到的授权码。注：不是QQ密码。
    # #subject = "python+smtp"  # 邮件主题
    # text = "send email"  # 邮件正文内容
    #
    # smtp = SMTP_SSL(hostname)  # SMTP_SSL默认使用465端口
    # smtp.login(login, password)
    #
    # msg = MIMEText(text, "plain", "utf-8")
    # msg["Subject"] = Header(subject, "utf-8")
    # msg["from"] = email_from
    # msg["to"] = email_to
    #
    # smtp.sendmail(email_from, email_to, msg.as_string())
    # smtp.quit()

ACCOUNT = input("ACCOUNT: ")
PASSWORD = input("PASSWORD: ")
print("-"*50)
options = webdriver.ChromeOptions()
mobile_emulation = {"deviceName": "iPhone X"}
option = webdriver.ChromeOptions()
# option.add_argument('headless')
# option.add_experimental_option('mobileEmulation', mobile_emulation)
mobile_driver = webdriver.Chrome(options=option)
# option.add_experimental_option('excludeSwitches', ['enable-automation'])     #打开开发者模式

# driver = webdriver.Chrome(chrome_options=options,executable_path="./chromedriver.exe")    #这个Chromedriver改过代码

mobile_driver.get('https://ais.usvisa-info.com/en-gb/niv/users/sign_in')
mobile_driver.find_element_by_xpath('/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[1]/input').send_keys(ACCOUNT)
mobile_driver.find_element_by_xpath('/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[2]/input').send_keys(PASSWORD)
mobile_driver.find_element_by_xpath('/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div').click()
mobile_driver.find_element_by_xpath('/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input').click()
#拿预约时间
time.sleep(2)
wb_data = mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;', '><').replace('&amp;', '&').strip()
soup = BeautifulSoup(wb_data, 'html.parser')
appointment_time = soup.select(".consular-appt")[0].get_text()
appointment_time = appointment_time.replace("Consular Appointment","").replace(" London local time at London","").replace("get directions","").replace("\n","").replace(": ","").replace(" —","").replace(":","")[:-12]
print(appointment_time)
try:
    mobile_driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
except:
    pass
mobile_driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/a').click()
time.sleep(2)
mobile_driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a').click()
time.sleep(1)
curent_month = appointment_time[2:].strip()

while(True):
    try:
        mobile_driver.find_element_by_xpath('/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[1]/input').click()
        time.sleep(1)
        #4月5月检测
        wb_data = mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;', '><').replace('&amp;', '&').strip()
        soup = BeautifulSoup(wb_data, 'html.parser')
        first = soup.select(".ui-datepicker-group.ui-datepicker-group-first")
        first = BeautifulSoup(str(first[0]), 'html.parser')
        month_first = first.select(".ui-datepicker-month")[0].get_text()
        print(month_first)
        try:
            avaliable = first.select("td > a")[0].get_text()
            print(avaliable)
            nonavaliable = first.select("tbody > tr > td")  # [0].get_text()
            count = 0
            for i in nonavaliable:
                if "span" not in str(i):
                    count += 1
                else:
                    break
            row = (int(avaliable) + int(count)) % 7
            line = int((int(avaliable) + int(count)) / 7) + 1
            tmp = "/html/body/div[5]/div[1]/table/tbody/tr[" + str(line) + "]/td[" + str(row) + "]/a"
            mobile_driver.find_element_by_xpath(tmp).click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input").click()
            if int(appointment_time[:2]) > int(avaliable) and ((month_dic[curent_month] - month_dic[first] <= 3) if (month_dic[curent_month] > month_dic[first]) else (month_dic[first] - month_dic[curent_month] + 12 <= 3)):
                mobile_driver.find_element_by_xpath("/html/body/div[6]/div/div/a[2]").click()
                curent_month = month_first
                #send_email(str(str(month_first) + " " + str(avaliable)))

        except:
            print([])

        last = soup.select(".ui-datepicker-group.ui-datepicker-group-last")
        last = BeautifulSoup(str(last[0]), 'html.parser')
        month_last = last.select(".ui-datepicker-month")[0].get_text()
        print(month_last)
        try:
            avaliable = last.select("td > a")[0].get_text()
            print(avaliable)
            nonavaliable = last.select("tbody > tr > td")  # [0].get_text()
            count = 0
            for i in nonavaliable:
                if "span" not in str(i):
                    count += 1
                else:
                    break
            row = (int(avaliable) + int(count)) % 7
            line = int((int(avaliable) + int(count)) / 7) + 1
            tmp = "/html/body/div[5]/div[2]/table/tbody/tr[" + str(line) + "]/td[" + str(row) + "]/a"
            mobile_driver.find_element_by_xpath(tmp).click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input").click()
            if int(appointment_time[:2]) > int(avaliable) and ((month_dic[curent_month] - month_dic[first] <= 2) if (month_dic[curent_month] > month_dic[first]) else (month_dic[first] - month_dic[curent_month] + 12 <= 2)):
                mobile_driver.find_element_by_xpath("/html/body/div[6]/div/div/a[2]").click()
                curent_month = month_last
                #send_email(str(str(month_last) + " " + str(avaliable)))
        except:
            print([])

        #6月7月检测
        mobile_driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/a/span').click()
        mobile_driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/a/span').click()
        time.sleep(2)
        wb_data = mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;', '><').replace(
            '&amp;', '&').strip()
        soup = BeautifulSoup(wb_data, 'html.parser')
        first = soup.select(".ui-datepicker-group.ui-datepicker-group-first")
        first = BeautifulSoup(str(first[0]), 'html.parser')
        month_first = first.select(".ui-datepicker-month")[0].get_text()
        print(month_first)
        try:
            avaliable = first.select("td > a")[0].get_text()
            print(avaliable)
            nonavaliable = first.select("tbody > tr > td")  # [0].get_text()
            count = 0
            for i in nonavaliable:
                if "span" not in str(i):
                    count += 1
                else:
                    break
            row = (int(avaliable) + int(count)) % 7
            line = int((int(avaliable) + int(count)) / 7) + 1
            tmp = "/html/body/div[5]/div[1]/table/tbody/tr[" + str(line) + "]/td[" + str(row) + "]/a"
            mobile_driver.find_element_by_xpath(tmp).click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input").click()
            if int(appointment_time[:2]) > int(avaliable) and ((month_dic[curent_month] - month_dic[first] <= 1) if (month_dic[curent_month] > month_dic[first]) else (month_dic[first] - month_dic[curent_month] + 12 <= 1)):
                mobile_driver.find_element_by_xpath("/html/body/div[6]/div/div/a[2]").click()
                curent_month = month_first
                #send_email(str(str(month_first) + " " + str(avaliable)))

        except:
            print([])

        last = soup.select(".ui-datepicker-group.ui-datepicker-group-last")
        last = BeautifulSoup(str(last[0]), 'html.parser')
        month_last = last.select(".ui-datepicker-month")[0].get_text()
        print(month_last)
        try:
            avaliable = last.select("td > a")[0].get_text()
            print(avaliable)
            nonavaliable = last.select("tbody > tr > td")  # [0].get_text()
            count = 0
            for i in nonavaliable:
                if "span" not in str(i):
                    count += 1
                else:
                    break
            row = (int(avaliable) + int(count)) % 7
            line = int((int(avaliable) + int(count)) / 7) + 1
            tmp = "/html/body/div[5]/div[2]/table/tbody/tr[" + str(line) + "]/td[" + str(row) + "]/a"
            mobile_driver.find_element_by_xpath(tmp).click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").click()
            mobile_driver.find_element_by_xpath(
                "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input").click()
            if int(appointment_time[:2]) > int(avaliable) and ((month_dic[curent_month] - month_dic[first] <= 0) if (month_dic[curent_month] > month_dic[first]) else (month_dic[first] - month_dic[curent_month] + 12 <= 0)):
                mobile_driver.find_element_by_xpath("/html/body/div[6]/div/div/a[2]").click()
                curent_month = month_last
                #send_email(str(str(month_last) + " " + str(avaliable)))
        except:
            print([])
        time.sleep(30)
        mobile_driver.refresh()
        time.sleep(2)

    except:
        wb_data = mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;', '><').replace(
            '&amp;', '&').strip()
        soup = BeautifulSoup(wb_data, 'html.parser')
        if "There are no available appointments at the selected location. Please try again later." in str(soup):
            print("not available")
            time.sleep(30)
            mobile_driver.refresh()
            time.sleep(3)
        elif "too many" in str(soup):
            print("too many request")
            time.sleep(60)
            mobile_driver.refresh()
            time.sleep(3)
        else:
            mobile_driver.get('https://ais.usvisa-info.com/en-gb/niv/users/sign_in')
            mobile_driver.find_element_by_xpath(
                '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[1]/input').send_keys(ACCOUNT)
            mobile_driver.find_element_by_xpath(
                '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[2]/input').send_keys(PASSWORD)
            mobile_driver.find_element_by_xpath(
                '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div').click()
            mobile_driver.find_element_by_xpath('/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input').click()
            # 拿预约时间
            time.sleep(2)
            wb_data = mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;',
                                                                                                  '><').replace('&amp;',
                                                                                                                '&').strip()
            soup = BeautifulSoup(wb_data, 'html.parser')
            appointment_time = soup.select(".consular-appt")[0].get_text()
            appointment_time = appointment_time.replace("Consular Appointment", "").replace(
                " London local time at London", "").replace("get directions", "").replace("\n", "").replace(": ",
                                                                                                            "").replace(
                " —", "").replace(":", "")[:-12]
            print(appointment_time)
            try:
                mobile_driver.find_element_by_xpath(
                    '/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
            except:
                pass
            mobile_driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/a').click()
            time.sleep(2)
            mobile_driver.find_element_by_xpath(
                '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a').click()
            time.sleep(1)
            curent_month = appointment_time[2:].strip()




input("please input any key to exit!")
