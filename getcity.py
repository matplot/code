# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time


def table_exists(con, table_name):
    cursor = con.cursor()
    cursor.execute('show tables')
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        # 存在返回1
        return 1
    else:
        # 不存在返回0
        cursor.execute("create table %s(house_type char(20),house_tag char(20),house_price int not null) "%table_name)


def one_page_code(user_in_city, city, cityn, con):
    global ab2, cd, jg2
    cursor = con.cursor()
    table_exists(con, cityn)
    url = 'https://' + user_in_city + '.lianjia.com/ershoufang/pg{}/'
    for a in range(1, 21):
        url1 = url.format(a)
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}
        page = requests.get(url1, headers=header)
        a = page.text
        soup = BeautifulSoup(a, "lxml")
        house_type = []
        house_tag = []
        house_price = []
        for b in soup.find_all('div', class_='info clear'):
            for ab in b.find_all('div', class_="houseInfo"):
                ab1 = ab.get_text()
                ab2 = re.findall(r"\d室\d厅", ab1)
                cd = re.findall(r"\D装|毛坯|其他", ab1)
                house_type.append(ab2[0])
                house_tag.append(cd[0])
                # print(house_type)
                # print(house_tag)
            for jg in b.find_all('div', class_='unitPrice'):
                jg1 = jg.get_text()
                jg2 = re.findall(r"\d+", jg1)
                house_price.append(jg2[0])
                # print(house_price)
        time.sleep(0.2)
        connent = pymysql.connect(host='localhost', port=3306, user='root', passwd='wjq', db='houseprice',
                                  charset='utf8')
        cursor = connent.cursor()

        for flag in range(len(house_price)):
            # sql = "insert into km(house_type,house_tag,house_price) values("%s" ,"%s",%s)"%(house_type[flag],house_tag[flag],house_price[flag])
            # print(sql)
            # se = cursor.mogrify('insert into km(house_type,house_tag,house_price) values("%s","%s",%s)' %(house_type[flag],house_tag[flag],house_price[flag]))
            # print(se)
            sql = 'insert into %s(house_type,house_tag,house_price) values("%s","%s",%s)' % (city, house_type[flag],
                                                                                             house_tag[flag],
                                                                                             house_price[flag])
            cursor.execute(sql)
            connent.commit()
    cursor.close()


def main():
    con = pymysql.Connect(host="localhost", user="root", passwd="wjq", database="houseprice", charset="utf8")
    user_in_city = input('输入爬取城市：')
    user_in_name = input('输入爬取城市名称拼写（创建的表名）：')
    user_in_cityn = input('输入要存入的表名:')
    one_page_code(user_in_city, user_in_name, user_in_cityn, con)


if __name__ == '__main__':
    main()
