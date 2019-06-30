#/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime

def main():
    datasets = []
    url = "https://lantouzi.com"
    res = requests.get(url)
    print("process: " + url)
    html = res.text        
    total = find_data(html)
    filepath = 'lantouzi_leiji.txt'
    line = "{0} : {1}".format(datetime.datetime.now(), total)
    with open(filepath, 'a') as wf:
        wf.write(line + "\n")

def find_data(html):
    soup = BeautifulSoup(html, "lxml")
    # body > section.sec-5 > div.home-stats > div > div > div:nth-child(4) > span.money
    total = soup.select_one("body > section.sec-5 > div.home-stats > div > div > div:nth-of-type(4) > span.money")
    return total.get_text()

if __name__ == '__main__':
    main()    
