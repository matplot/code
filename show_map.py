from pyecharts import options as opts
from pyecharts.charts import Map
import pymysql

def main():
    con = pymysql.Connect(host="localhost", user="root", passwd="wjq", database="houseprice", charset="utf8")
    cursor = con.cursor()
    province = ['北京', '吉林', '湖南', '四川', '重庆', '福建', '广东', '贵州', '黑龙江', '海南',
                '浙江', '安徽', '内蒙古',
                '山东', '云南', '甘肃', '江西', '江苏', '广西', '上海', '辽宁', '河北',
                '山西', '天津', '湖北',
                '新疆', '陕西', '宁夏', '河南']
    cursor.execute('select price from avg1')
    data = cursor.fetchall()
    data_show = [(province[i], data[i]) for i in range(len(province))]

    _map = (
        Map(init_opts=opts.InitOpts(width="480px",height="320px", bg_color="rgba(0,0,255,0.1)"))
            .add("房价", data_show, "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map"),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(max_=60000, min_=0, is_piecewise=True),
        )
    )

    _map.render(path="re1.html")

if __name__ == '__main__':
    main()