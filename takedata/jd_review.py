#/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def main():
    datasets = []

    link_template = "https://club.jd.com/comment/skuProductPageComments.action?productId=7651925&score=0&sortType=6&pageSize=10&isShadowSku=0&fold=1&page="

    for page in range(0, 10000):
        link = link_template + str(page)
        res = requests.get(link, headers={'referer': 'https://item.jd.com/7651925.html'})
        print("process: " + link)
        html = res.text 
        dataset = find_data(html)
        print("get data count: " + str(len(dataset)))

        if len(dataset) <= 0:
            print(html)
            break

        datasets.extend(dataset)

    pd_data = pd.DataFrame(datasets)
    pd_data.to_csv("review.csv", encoding='utf-8-sig')

def find_data(html):
    data = json.loads(html)
    dataset = []
    headers = ['id', 'guid', 'content', 'creationTime', 'score', 'productColor', 'productSize', 'nickname', 'firstCategory', 'secondCategory', 'thirdCategory']

    if not 'comments' in data:
        return dataset

    for comment in data['comments']:
        fields = []
        for header in headers:
            if header in comment:
                fields.append(str(comment[header]).strip())
            else:
                fields.append('')
        dataset.append(dict(zip(headers, fields)))    

    return dataset


def check_end(html):
    pass

if __name__ == '__main__':    
    main()    