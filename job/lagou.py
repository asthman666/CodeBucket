# -*- coding: utf-8 -*-

import time
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

seen = {}

def main():
    driver = webdriver.Chrome()

    url = 'https://www.lagou.com/jobs/list_?px=new&yx=15k-25k&city=%E8%A5%BF%E5%AE%89&district=%E9%AB%98%E6%96%B0%E6%8A%80%E6%9C%AF%E4%BA%A7%E4%B8%9A%E5%BC%80%E5%8F%91%E5%8C%BA#order'
    driver.get(url)   
    source_html = driver.page_source
    find_company_name(source_html)

    RUN = 1
    while RUN:
        ele = driver.find_element_by_css_selector("span[hidefocus='hidefocus'][action='next']")
        #print(ele.text)
        #print(ele.get_attribute("class"))
        if (ele.get_attribute("class") == "pager_next pager_next_disabled"):
            RUN = 0
        else:
            ele.click()
            time.sleep(5)
            source_html = driver.page_source
            find_company_name(source_html)

def find_company_name(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')
    lists = soup.find("div", attrs={"id": "s_position_list"})
    #print(lists)
    for lst in lists.find("ul", attrs={"class": "item_con_list"}).find_all("li"):
        company_name = lst.find("div", attrs={"class": "company_name"}).find("a").get_text()
        seen[company_name] = seen.get(company_name, 0) + 1
        print(company_name)

if __name__ == '__main__':
    main()
    for i in sorted(seen.items(), key=lambda x: x[1], reverse=True):
        print(i)