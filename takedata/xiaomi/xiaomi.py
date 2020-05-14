# -*- coding: utf-8 -*-

import time
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()
#data_attr = ["item_name", "image_link", "review_count", "review_rate", "price", "comment_url", "product_id"]
data_attr = ["review_count", "review_rate", "comment_url"]

item_details = []

def main():
    url = 'https://www.mi.com/'
    driver.get(url)   
    source_html = driver.page_source
    category_links = []
    category_links.extend(find_category_links(source_html))

    detail_links = []
    for category_link in category_links:
        driver.get(category_link)
        source_html = driver.page_source
        time.sleep(10)
        detail_links.extend(find_detail_links(source_html))
        break

    for dl in detail_links:
        detail(dl)
        #break

    driver.close()

    pd_data = pd.DataFrame(item_details, columns=data_attr)
    pd_data.to_csv("item.csv")                

def find_category_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')
    lists = soup.find("ul", attrs={"id": "J_categoryList"})
    category_links = []

    for lst in lists.find_all("li", attrs={"class": "category-item"}):
        for li in lst.select("ul[class^='children-list'] li"):
            href = li.select_one("a").get('href')
            if not re.search('search.mi.com', href, re.I) is None:
                category_links.append("https:" + href)

    #print(category_links)
    return category_links

def find_detail_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')
    lists = soup.find("div", attrs={"id": "J_goodsList"})

    detail_links = []
    for lst in lists.find_all("div", attrs={"class": "goods-item"}):
        detail_links.append("https://www.mi.com/comment/" + lst.get('data-productid') + '.html')
    #print(detail_links)
    return detail_links

def detail(detail_url):
    driver.get(detail_url)
    source_html = driver.page_source
    #print(source_html)
    soup = BeautifulSoup(source_html, 'html.parser')

    datas = []
    datas.append(soup.select_one("div[class='m-t'] span").get_text())
    rate = soup.select_one("div[class='m-b'] span").get_text()
    datas.append(re.sub('[^\d\.%]', '', rate))
    datas.append(detail_url)
    item_details.append(dict(list(zip(data_attr, datas))))
    time.sleep(8)

if __name__ == '__main__':
    main()
