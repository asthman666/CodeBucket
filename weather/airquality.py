#/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import datetime
import os
import config
import pytz

class AirQuality(object):
    def extract_data(self, url):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                    'Referer': 'https://weather.com/',
                    'Upgrade-Insecure-Requests': '1'
        }
        f = requests.get(url, headers=headers)
        web_content = f.text        
        with open('web_file/{}-{}.txt'.format("airquality", datetime.date.today().isoformat()), 'w', encoding='utf8') as file:
            file.write(web_content)
        
        soup = BeautifulSoup(web_content, 'lxml')
        datas = {"column_headers": ['name', 'unit', 'num', 'desc'],
                 "column_datas": []
        }

        names = []
        units = []
        descs = []
        nums = []

        for name in soup.select_one('div[class^="AirQuality--allPollutantDials"]').select('span[class*="AirQuality--pollutantName"]'):
            names.append(name.get_text())
            #print(name.get_text())

        for name in soup.select('span[class*="AirQuality--pollutantMeasurement"]'):
            units.append(name.get_text())            
            #print(name.get_text())
        
        for desc in soup.select('p[class*="AirQuality--pollutantCategory"]'):
            descs.append(desc.get_text())
            #print(desc.get_text())

        for num in soup.select('text[class*="AirQuality--pollutantDialText"]'):
            nums.append(num.get_text())
            #print(num.get_text())

        if len(names) == len(descs) and len(names) == len(nums):
            for i in range(0, len(names)):
                primary = 0
                if i == 0:
                    primary = 1
                datas['column_datas'].append([names[i], units[i], nums[i], descs[i], primary])
        
        return datas

if __name__ == '__main__':
    url = 'https://weather.com/zh-CN/forecast/air-quality/l/CHXX0141:1:CH'
    airq = AirQuality()
    datas = airq.extract_data(url)
    print(datas)
    