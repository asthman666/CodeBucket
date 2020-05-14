# -*- coding: utf-8 -*-

import time
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()
data_attr = ["item_name", "image_link", "review_count", "review_rate", "price"]
item_details = []

def main():
    url = 'https://m.mi.com/category'
    driver.get(url)   
    source_html = driver.page_source
    detail_links = []
    detail_links.extend(find_detail_links(source_html))

    RUN = 1
    while RUN:
        ele = driver.find_element_by_css_selector("span[hidefocus='hidefocus'][action='next']")
        #print(ele.text)
        #print(ele.get_attribute("class"))
        if (ele.get_attribute("class") == "pager_next pager_next_disabled"):
            RUN = 0
        else:
            ele.click()
            time.sleep(10)
            source_html = driver.page_source
            detail_links.extend(find_detail_links(source_html))
            #break

    for dl in detail_links:
        detail(dl)
        #break
    driver.close()

    pd_data = pd.DataFrame(job_details, columns=data_attr)
    pd_data.to_csv("job_details_25-50.csv")                

def find_category_links(source_html):
    

def find_detail_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')
    lists = soup.find("div", attrs={"id": "s_position_list"})

    detail_links = []
    for lst in lists.find("ul", attrs={"class": "item_con_list"}).find_all("li"):
        detail_link = lst.select_one("a[class='position_link']").get('href')
        detail_links.append(detail_link)
    #print(detail_links)
    return detail_links

def detail(detail_url):
    driver.get(detail_url)
    source_html = driver.page_source
    #print(source_html)
    soup = BeautifulSoup(source_html, 'html.parser')
    datas = []
    # data_attr = ["company_name", "position", "salary", "location", "experience", "education", "time", "location_detail", "keyword", "description", "position_link"]
    datas.append(soup.find("div", "job-name").find("h4", "company").get_text())
    datas.append(soup.find("div", attrs={"class": "job-name"}).find("h1", attrs={"class": "name"}).get_text())
    datas.append(soup.find("dd", attrs={"class": "job_request"}).find("span", attrs={"class": "salary"}).get_text())
    datas.append(soup.select_one("dd[class='job_request'] span:nth-of-type(2)").get_text().replace('/', ''))
    datas.append(soup.select_one("dd[class='job_request'] span:nth-of-type(3)").get_text().replace('/', ''))
    datas.append(soup.select_one("dd[class='job_request'] span:nth-of-type(4)").get_text().replace('/', ''))
    datas.append(soup.select_one("dd[class='job_request'] span:nth-of-type(5)").get_text())
    keywords = []
    for k in soup.select("ul[class^='position-label'] li"):
        keywords.append(k.get_text())
    datas.append(soup.select_one("div[class='work_addr']").get_text().replace('查看地图', ''))
    datas.append(','.join(keywords))
    datas = [re.sub('\s+', '', d) for d in datas]
    datas.append(soup.select_one("div[class='job-detail']").get_text().strip())
    datas.append(detail_url)
    job_details.append(dict(list(zip(data_attr, datas))))
    time.sleep(8)

if __name__ == '__main__':
    main()
