# -*- coding: utf-8 -*-

import time
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()
data_attr = ["product_id", "title", "image_url", "price", "comment_url", "review_count", "review_rate"]

item_details = []

def main():
    url = 'https://www.mi.com/'
    driver.get(url)   
    source_html = driver.page_source
    category_links = []
    category_links.extend(find_category_links(source_html))

    #return

    detail_links = []
    partial_detail_datas = []
    for category_link in category_links:
        driver.get(category_link)
        source_html = driver.page_source
        time.sleep(10)
        (partial_detail_links, partial_detail_data) = find_detail_links(source_html)
        #print(partial_detail_data)
        detail_links.extend(partial_detail_links)
        partial_detail_datas.extend(partial_detail_data)
        #break

    data_batch_index = 0
    index = 0
    batch_size = 100
    for dl in detail_links:
        detail(dl, partial_detail_datas[index])
        if (len(item_details) % batch_size == 0):
            start = data_batch_index * batch_size
            end = data_batch_index * batch_size + batch_size
            pd_data = pd.DataFrame(item_details[start:end], columns=data_attr)
            pd_data.to_csv("item{index}.csv".format(index=data_batch_index), encoding='utf-8-sig') 
            data_batch_index = data_batch_index + 1
        index = index + 1
        #break

    if (len(item_details) % batch_size != 0):
        start = data_batch_index * batch_size
        end = data_batch_index * batch_size + len(item_details) % batch_size
        pd_data = pd.DataFrame(item_details[start:end], columns=data_attr)
        pd_data.to_csv("item{index}.csv".format(index=data_batch_index), encoding='utf-8-sig')                

    driver.close()          
    pd_data = pd.DataFrame(item_details, columns=data_attr)
    pd_data.to_csv("item.csv", encoding='utf-8-sig')          

def find_category_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')
    lists = soup.find("ul", attrs={"id": "J_categoryList"})
    category_links = []

    for lst in lists.find_all("li", attrs={"class": "category-item"}):
        for li in lst.select("ul[class^='children-list'] li"):
            href = li.select_one("a").get('href')
            #print(href)
            if re.search('search.mi.com', href, re.I):
                if re.match('https', href, re.I):
                    category_links.append(href)
                else:
                    category_links.append("https:" + href)

    #print(category_links)
    return category_links

def find_detail_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')
    lists = soup.find("div", attrs={"id": "J_goodsList"})

    detail_links = []
    tmp_data = []
    for lst in lists.find_all("div", attrs={"class": "goods-item"}):
        product_id = lst.get('data-productid')
        title = lst.select_one("h2[class='title']").get_text()
        image_url = lst.select_one("img").get("src")
        price = lst.select_one("p[class='price']").find(text=True)
        #print(price)
        price = re.sub('[^\d.,]', '', price)
        comment_url = "https://www.mi.com/comment/" + lst.get('data-productid') + ".html"
        tmp_data.append([product_id, title, image_url, price, comment_url])
        detail_links.append(comment_url)
    #print(detail_links)
    return (detail_links, tmp_data)

def detail(detail_url, datas):
    driver.get(detail_url)
    source_html = driver.page_source
    #print(source_html)
    soup = BeautifulSoup(source_html, 'html.parser')

    # no comment case: https://www.mi.com/comment/11655.html
    # no comment case: https://www.mi.com/comment/12010.html
    if (not soup.select_one("div[class='none']") and soup.select_one("div[class='m-t'] span")):
        datas.append(soup.select_one("div[class='m-t'] span").get_text())
        rate = soup.select_one("div[class='m-b'] span").get_text()
        datas.append(re.sub('[^\d\.]', '', rate))
        datas = [re.sub('\s+', '', d) for d in datas]
        item_details.append(dict(list(zip(data_attr, datas))))
    else:
        print("no data found for url: {0}".format(detail_url))
    time.sleep(15)

if __name__ == '__main__':
    main()
