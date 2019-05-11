#/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    datasets = []
    for page in range(1, 1000):
        res = requests.get("https://lantouzi.com/platform_data/" + str(page))
        print("process: " + "https://lantouzi.com/platform_data/" + str(page))
        html = res.text        
        if check_end(html):
            break
        dataset = find_data(html)
        datasets.append(dataset)

    pd_data = pd.DataFrame(datasets)
    pd_data.to_csv("grab.csv")

def find_data(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", attrs={"class":"g-table"})

    headers = []
    fields = []

    for row in table.find_all("tr")[1:]:
        index = 0
        for td in row.find_all("td"):
            if index == 0:
                headers.append(td.get_text())
                index = index + 1
            else:
                fields.append(td.get_text())

    return dict(zip(headers, fields))

def check_end(html):
    return '往期运营数据' in html

if __name__ == '__main__':
    main()    