#/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql.cursors
import config
import datetime
from weather import Weather

def save2db(datas):
    dt_fetch = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Connect to the database
    connection = pymysql.connect(host=config.db['host'],
                                user=config.db['user'],
                                password=config.db['password'],
                                db=config.db['db'],
                                charset=config.db['charset'],
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for d in datas['column_datas']:
                (low_temp, high_temp) = d[2].split('/')
                sql = "INSERT INTO `weather` (`dt_fetch`, `dt`, `weather`, `low_temp`, `high_temp`, `rain_rate`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (dt_fetch, d[0], d[1], low_temp, high_temp, d[3]))
        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    url = 'https://weather.com/weather/5day/l/CHXX0141:1:CH'
    weather = Weather()
    datas = weather.get_datas(url)
    #print(datas)    
    save2db(datas)