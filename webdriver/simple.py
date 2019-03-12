import time
from selenium import webdriver
from json import JSONEncoder, JSONDecoder

driver = webdriver.Chrome()

url = 'https://passport.jd.com/new/login.aspx'
driver.get(url)

cookie = ''
with open("cookie.txt", 'r', encoding = 'utf8') as file:
    cookie = file.read()

cookies = JSONDecoder().decode(cookie)

for c in cookies:
    print(c)
    driver.add_cookie(c)


#cur_cookies = driver.get_cookies()
#print(cur_cookies)
'''
time.sleep(30)

cur_cookies = driver.get_cookies()
with open('cookie.txt', 'w', encoding='utf8') as file:
    print("write to file begin")
    cookie_str = JSONEncoder().encode(cur_cookies)
    file.write(cookie_str)
    print("write {}".format(cur_cookies))
    print("write to file end")
'''