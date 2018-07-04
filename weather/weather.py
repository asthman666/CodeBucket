#/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import traceback
import datetime
import os
import config
import smtplib
from email.mime.text import MIMEText  
import jinja2
import rsa

class Weather(object):
    translate = {'AM Thunderstorms':u'上午雷暴', 
                 'PM Thunderstorms':u'下午雷暴', 
                 'Sunny':u'晴天', 
                 'Mostly Sunny':u'晴天', 
                 'Partly Cloudy':u'多云', 
                 'Cloudy': u'多云',
                 'AM Showers':u'上午阵雨'}
    translate = {}                 
    
    def temp_calculate(self, temp):
        return int(round((int(temp) - 32)/1.8))        

    def temp_extract(self, temp_string):
        if temp_string == '--':
            return '--'
        return re.search(r'\d+', temp_string).group()

    def get_datas(self, url):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                    'Referer': 'https://weather.com/',
                    'Upgrade-Insecure-Requests': '1'
        }
        f = requests.get(url, headers=headers)
        text = f.text

        if not os.path.exists('web_file'):
            os.makedirs('web_file')

        with open('web_file/{}.txt'.format(datetime.date.today().isoformat()), 'w', encoding='utf8') as file:
            file.write(text)
        
        weather_report = ''
        soup = BeautifulSoup(text, 'lxml')
        datas = {"column_headers": ['DAY', 'DESCRIPTION', 'LOW/HIGH', 'PRECIP'],
                 "column_datas": []
        }
        for num in range(1,6):
            date = (datetime.date.today()+datetime.timedelta(days=(num-1))).isoformat()
            
            weather_selector = "#twc-scrollabe > table > tbody > tr:nth-of-type({}) > td.description > span".format(num)
            weather = soup.select_one(weather_selector).get_text()

            highest_temperature_selector = "#twc-scrollabe > table > tbody > tr:nth-of-type({}) > td.temp > div > span:nth-of-type(1)".format(num)
            lowest_temperature_selector = "#twc-scrollabe > table > tbody > tr:nth-of-type({}) > td.temp > div > span:nth-of-type(3)".format(num)

            highest_temperature = soup.select_one(highest_temperature_selector).get_text()
            highest_temperature = self.temp_extract(highest_temperature)

            lowest_temperature = soup.select_one(lowest_temperature_selector).get_text()
            lowest_temperature = self.temp_extract(lowest_temperature)

            if highest_temperature != '--':
                highest_temperature = self.temp_calculate(highest_temperature)
            lowest_temperature = self.temp_calculate(lowest_temperature)
            rain_rate_selector = "#twc-scrollabe > table > tbody > tr:nth-of-type({}) > td.precip > div > span:nth-of-type(2) > span".format(num)
            rain_rate = soup.select_one(rain_rate_selector).get_text()

            if weather in self.translate:
                weather = self.translate[weather]

            datas["column_datas"].append([date, weather, str(lowest_temperature) + '/' + str(highest_temperature), rain_rate])
        return datas

    def generate_report(self, datas):
        return ReportHTML.generate_html(datas)

class Email(object):
    user_name = ''
    password = ''
    smtpserver = ''
    def __init__(self, username, password, smtpserver):
        self.username = username
        self.smtpserver = smtpserver
        self.smtp = smtplib.SMTP()  
        self.smtp.connect(smtpserver)  
        self.smtp.login(username, password)  
    
    def send_mail(self, **email):
        #print(email)
        try:
            msg = MIMEText(email['msg'], 'html', 'utf-8')
            msg['Subject'] = email['subject']
            msg['From'] = self.username
            msg['To'] = ", ".join(email['to'])
            self.smtp.sendmail(self.username, email['to'], msg.as_string())  
        except Exception as e:
            print("send mail failed, reason: " + str(e))
            traceback.print_exc()
        finally:
            self.smtp.quit()  

class ReportHTML(object):
    @staticmethod
    def generate_html(datas):
        template_filename = "./template/weather.html"
        script_path = os.path.dirname(os.path.abspath(__file__))
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))   
        t = environment.get_template(template_filename).render(data_headers=['DAY', 'DESCRIPTION', 'LOW/HIGH', 'PRECIP'],datas=datas)
        return t

if __name__ == '__main__':
    url = 'https://weather.com/weather/5day/l/CHXX0141:1:CH'
    weather = Weather()
    datas = weather.get_datas(url)
    weather_report = weather.generate_report(datas)

    #print(weather_report)
    #quit()

    print("Do you want to get report to email(Y/N)?")
    is_email = input()

    if is_email == 'Y':
        with open('./key.pem', mode='rb') as privfile:
            keydata = privfile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)
        crypto = rsa.transform.int2bytes(int(config.password))
        password = rsa.decrypt(crypto, privkey)
            
        email = Email(config.smtp['username'], password.decode('utf8'), config.smtp['smtpserver'])
        email.send_mail(msg=weather_report, to=config.to, subject=config.email['subject'])



