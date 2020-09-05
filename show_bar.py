from pyecharts.charts import Bar
from pyecharts import options as opts
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
        cursor.execute("create table %s(tag char(50),price char(50)) "%table_name)

def get_data(con):
    type = ['毛坯','精装','简装']
    city = ['北京', '上海', '广东']
    tablename = ['beijing', 'shanghai', 'guangzhou']
    create = ['bjhouse', 'shhouse', 'gdhouse']
    for i in range(len(city)):
        table_exists(con, create[i])
        cursor = con.cursor()
        for j in range(len(type)):
            cursor.execute('insert into %s select count(house_tag),avg(house_price) from %s where house_tag = "%s"'%(create[i],tablename[i],type[j]))
        cursor.execute('select tag from %s' % create[i])
        data1 = cursor.fetchall()
        #print(data1)
        cursor.execute('select price from %s' % create[i])
        data2 = cursor.fetchall()
        # print(data2)
        data3 = []
        data4 = []
        for j in range(len(data1)):
            data3.append(float((data1[j][0])))
            data4.append(float((data2[j][0])))
        cate = ['毛坯', '精装', '简装']
        # print(data3)
        # print(cate)
        print(data3)
        print(data4)

        # 1.x版本支持链式调用
        bar = (Bar(init_opts=opts.InitOpts(width="455px",height="230px",bg_color="rgba(0,0,255,0.1)"))
               .add_xaxis(cate)
               .add_yaxis('房源数量', data3)
               .add_yaxis('房价',data4)
               .set_global_opts(title_opts=opts.TitleOpts(title="%s" % city[i], subtitle=""))
              )
        # 在jupyter notebook总渲染
        k = i+3
        bar.render(path="%s.html"%k)
        cursor.close()

def main():
    con = pymysql.Connect(host="localhost", user="root", passwd="wjq", database="houseprice", charset="utf8")
    get_data(con)
if __name__ == '__main__':
    main()
