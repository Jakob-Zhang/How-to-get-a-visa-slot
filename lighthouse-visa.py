from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebDriver(object):
    mobile_driver = None
    appointment_time = None
    current_month = None
    month_dic = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                 "September": 9, "October": 10, "November": 11, "December": 12}

    def __init__(self):
        print("-" * 50)
        self.account = input("ACCOUNT: ")
        self.password =  input("PASSWORD: ")
        self.flag = input("Do you want to send you email to notify you?(yes/no)")
        if self.flag == "yes":
            self.email_from = input("email:")
            self.password = input("password:")
            #self.email_to = input("email to:")
            self.hostname = input("hostname:")
        if self.flag is None or self.flag == "no":
            pass
        print("-" * 50)

    def send_email(self, subject):
        from smtplib import SMTP_SSL
        from email.mime.text import MIMEText
        from email.header import Header
        self.login = self.email_from
        email_from = ""  # 改为自己的发送邮箱
        email_to = ""  # 接收邮箱
        hostname = "smtp.qq.com"  # 不变，QQ邮箱的smtp服务器地址
        login = ""  # 发送邮箱的用户名
        password = ""  # 发送邮箱的密码，即开启smtp服务得到的授权码。注：不是QQ密码。
        # subject = "python+smtp"  # 邮件主题
        text = "succeed"  # 邮件正文内容

        smtp = SMTP_SSL(self.hostname)  # SMTP_SSL默认使用465端口
        smtp.login(self.login, self.password)

        msg = MIMEText(text, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["from"] = self.email_from
        msg["to"] = self.email_to

        smtp.sendmail(self.email_from, self.email_to, msg.as_string())
        smtp.quit()

    def chrome_init(self):
        mobile_emulation = {"deviceName": "iPhone X"}
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # option.add_experimental_option('mobileEmulation', mobile_emulation)
        self.mobile_driver = webdriver.Chrome(options=option)
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])     #打开开发者模式
        # driver = webdriver.Chrome(chrome_options=options,executable_path="./chromedriver.exe")    #这个Chromedriver改过代码

    def sign_in(self):
        self.mobile_driver.get('https://ais.usvisa-info.com/en-gb/niv/users/sign_in')
        self.mobile_driver.find_element(By.XPATH,
                                        '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[1]/input').send_keys(
            self.account)
        self.mobile_driver.find_element(By.XPATH,
                                        '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[2]/input').send_keys(
            self.password)
        self.mobile_driver.find_element(By.XPATH,
                                        '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div').click()
        self.mobile_driver.find_element(By.XPATH,
                                        '/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input').click()

    def get_appointment_time(self):
        time.sleep(2)
        wb_data = self.mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;',
                                                                                                   '><').replace(
            '&amp;', '&').strip()
        soup = BeautifulSoup(wb_data, 'html.parser')
        self.appointment_time = soup.select(".consular-appt")[0].get_text()
        self.appointment_time = self.appointment_time.replace("Consular Appointment", "").replace(
            " London local time at London", "").replace("get directions", "").replace("\n", "").replace(": ",
                                                                                                        "").replace(
            " —", "").replace(":", "")[:-12]
        print(self.appointment_time)
        try:
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
        except:
            pass
        self.mobile_driver.find_element(By.XPATH, '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/a').click()
        time.sleep(2)
        self.mobile_driver.find_element(By.XPATH,
                                        '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a').click()
        time.sleep(1)
        self.current_month = self.appointment_time[2:].strip()

    def something_wrong(self):
        wb_data = self.mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;',
                                                                                                   '><').replace(
            '&amp;', '&').strip()
        soup = BeautifulSoup(wb_data, 'html.parser')
        if "There are no available appointments at the selected location. Please try again later." in str(soup):
            print("not available")
            time.sleep(30)
            self.mobile_driver.refresh()
            time.sleep(3)
        elif "too many" in str(soup):
            print("too many request")
            time.sleep(60)
            self.mobile_driver.refresh()
            time.sleep(3)
        else:
            self.mobile_driver.get('https://ais.usvisa-info.com/en-gb/niv/users/sign_in')
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[1]/input').send_keys(
                self.account)
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[2]/input').send_keys(
                self.password)
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div').click()
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input').click()
            # 拿预约时间
            time.sleep(2)
            wb_data = self.mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;',
                                                                                                       '><').replace(
                '&amp;',
                '&').strip()
            soup = BeautifulSoup(wb_data, 'html.parser')
            self.appointment_time = soup.select(".consular-appt")[0].get_text()
            self.appointment_time = self.appointment_time.replace("Consular Appointment", "").replace(
                " London local time at London", "").replace("get directions", "").replace("\n", "").replace(
                ": ",
                "").replace(
                " —", "").replace(":", "")[:-12]
            print(self.appointment_time)
            try:
                self.mobile_driver.find_element(By.XPATH,
                                                '/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
            except:
                pass
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/a').click()
            time.sleep(2)
            self.mobile_driver.find_element(By.XPATH,
                                            '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a').click()
            time.sleep(1)
            self.current_month = self.appointment_time[2:].strip()

    def fresh_windows(self, month_time=4):
        self.mobile_driver.find_element(By.XPATH,
                                        '/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[1]/input').click()
        time.sleep(1)

        wb_data = self.mobile_driver.page_source.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;lt;',
                                                                                                   '><').replace(
            '&amp;', '&').strip()
        soup = BeautifulSoup(wb_data, 'html.parser')
        first = soup.select(".ui-datepicker-group.ui-datepicker-group-first")
        first = BeautifulSoup(str(first[0]), 'html.parser')
        month_first = first.select(".ui-datepicker-month")[0].get_text()
        print(month_first)
        try:
            available = first.select("td > a")[0].get_text()
            print(available)
            nonviable = first.select("tbody > tr > td")  # [0].get_text()
            count = 0
            for i in nonviable:
                if "span" not in str(i):
                    count += 1
                else:
                    break
            row = (int(available) + int(count)) % 7
            line = int((int(available) + int(count)) / 7) + 1
            tmp = "/html/body/div[5]/div[1]/table/tbody/tr[" + str(line) + "]/td[" + str(row) + "]/a"
            self.mobile_driver.find_element(By.XPATH, tmp).click()
            self.mobile_driver.find_element(By.XPATH,
                                            "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select").click()
            self.mobile_driver.find_element(By.XPATH,
                                            "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").click()
            self.mobile_driver.find_element(By.XPATH,
                                            "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input").click()
            if int(self.appointment_time[:2]) > int(available) and (
                    (self.month_dic[self.current_month] - self.month_dic[first] <= month_time - 1) if (
                            self.month_dic[self.current_month] > self.month_dic[first]) else (
                            self.month_dic[first] - self.month_dic[self.current_month] + 12 <= month_time - 1)):
                self.mobile_driver.find_element(By.XPATH, "/html/body/div[6]/div/div/a[2]").click()
                self.current_month = month_first
                if self.flag == "yes":
                    self.send_email(str(str(month_first) + " " + str(available)))
                print("Succeed")
                input("please input any key to exit!")
                return


        except:
            print([])

        last = soup.select(".ui-datepicker-group.ui-datepicker-group-last")
        last = BeautifulSoup(str(last[0]), 'html.parser')
        month_last = last.select(".ui-datepicker-month")[0].get_text()
        print(month_last)
        try:
            available = last.select("td > a")[0].get_text()
            print(available)
            nonviable = last.select("tbody > tr > td")  # [0].get_text()
            count = 0
            for i in nonviable:
                if "span" not in str(i):
                    count += 1
                else:
                    break
            row = (int(available) + int(count)) % 7
            line = int((int(available) + int(count)) / 7) + 1
            tmp = "/html/body/div[5]/div[2]/table/tbody/tr[" + str(line) + "]/td[" + str(row) + "]/a"
            self.mobile_driver.find_element(By.XPATH, tmp).click()
            self.mobile_driver.find_element(By.XPATH,
                                            "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select").click()
            self.mobile_driver.find_element(By.XPATH,
                                            "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").click()
            self.mobile_driver.find_element(By.XPATH,
                                            "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input").click()
            if int(self.appointment_time[:2]) > int(available) and (
                    (self.month_dic[self.current_month] - self.month_dic[first] <= month_time - 2) if (
                            self.month_dic[self.current_month] > self.month_dic[first]) else (
                            self.month_dic[first] - self.month_dic[self.current_month] + 12 <= month_time - 2)):
                self.mobile_driver.find_element(By.XPATH, "/html/body/div[6]/div/div/a[2]").click()
                self.current_month = month_last
                if self.flag == "yes":
                    self.send_email(str(str(month_last) + " " + str(available)))
                print("Succeed")
                input("please input any key to exit!")
                return
        except:
            print([])

    def init_driver(self):
        self.chrome_init()

        self.sign_in()

        self.get_appointment_time()

        while True:
            try:
                self.fresh_windows(4)
                self.mobile_driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/a/span').click()
                self.mobile_driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/a/span').click()
                self.fresh_windows(2)
            except:
                self.something_wrong()


if __name__ == "__main__":
    chrome = WebDriver()
    chrome.init_driver()
