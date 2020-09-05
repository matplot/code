import pymysql
import re


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
        cursor.execute("create table %s(price char(50)) "%table_name)


def get_avg(con, table):
    cur = con.cursor()
    table_exists(con, table)
    city = ['beijing', 'changchun', 'changsha', 'chengdu', 'chongqing', 'fuzhou', 'guangzhou', 'guiyang', 'haerbing',
            'haikou',
            'hangzhou', 'hefei', 'huhehaote',
            'jinan', 'kunming', 'lanzhou', 'nanchang', 'nanjing', 'nanning', 'shanghai', 'shenyang', 'shijiazhuang',
            'taiyuan', 'tianjing', 'wuhan',
            'wulumuqi', 'xian', 'yinchuan', 'zhenzhou']
    for i in range(len(city)):
        # cur.execute("select avg(house_price) from %s "% city[i])
        cur.execute("insert into %s select avg(house_price) from  %s" % (table,city[i]))
        print("success")
        # print(cur.fetchone().[i])


def main():
    con = pymysql.Connect(host="localhost", user="root", passwd="wjq", database="houseprice", charset="utf8")
    table = input('请输入创建的表名：')
    get_avg(con, table)


if __name__ == '__main__':
    main()
