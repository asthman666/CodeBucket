import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import pdfkit
import os

def find_link(url):
    source_html = requests.get(url).text
    #print(source_html)
    soup = BeautifulSoup(source_html, 'html.parser')
    links = []
    for li in soup.select_one("div[id='contents']").select_one("div:nth-of-type(2)").select("li[class='toctree-l2']"):
        href = li.select_one("a")['href']
        links.append(urljoin(url, href))
    return links

def generate_pdf(links):
    folders = []
    index = 1
    for link in links:
        #print(link)
        match = re.search(r'en/latest/(.+?)/', link)
        fold = match.group(1)

        if fold not in folders:
            folders.append(fold)
            index = 1

        match = re.search(r'en/latest/.+?/(.+?)\.html', link)
        name = match.group(1)
        name = name.replace('/', '-')

        if not os.path.exists(fold):
            os.makedirs(fold)        

        out_file = '{}/{}-{}.pdf'.format(fold, index, name)
        index = index + 1
        pdfkit.from_url(link, out_file)

if __name__ == '__main__':
    links = find_link('http://docs.celeryproject.org/en/latest/')
    generate_pdf(links)