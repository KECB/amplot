import pandas as pd
from amplot import MassPlotter
from amplot import Heatmap
import json

with open('key', 'r') as f:
    amap_key = f.readline()


def generat_mass_map():
    """
    海量数据格式
    [{"lnglat":[116.258446,37.686622],"name":"景县","style":2},
     {"lnglat":[113.559954,22.124049],"name":"圣方济各堂区","style":2},
     {"lnglat":[116.366794,39.915309],"name":"西城区","style":2},
     ...
     {"lnglat":[114.462931,38.028383],"name":"桥西区","style":2}
    ]
    """
    # step 1 地图
    amap = MassPlotter(amap_key, '51.512923', '-0.113524', zoom=9)

    # step 2 读取数据
    data = pd.read_csv('london-street.csv')
    bike_data = data[data['Crime type'] == 'Bicycle theft']
    # 去掉空数据项
    bike_data_location = bike_data[bike_data['Latitude'].isnull() == False]
    bike_data_2017 = bike_data_location[bike_data_location['Month'] == "2017-01"]
    mass_data = []

    for _, row in bike_data_2017.iterrows():
        try:
            item = {"lnglat": [row['Longitude'], row['Latitude']],
                    "name": row['Last outcome category'], "style": 2}
            mass_data.append(item)
        except:
            print('%s Key 不存在' % _)
    amap.add_mass_marker(mass_data)
    # step3 为数据增加样式属性
    style = "[{url: 'http://a.amap.com/jsapi_demos/static/images/mass0.png'," \
            "anchor: new AMap.Pixel(6, 6)," \
            "size: new AMap.Size(11, 11)" \
            "},{" \
            "url: 'http://a.amap.com/jsapi_demos/static/images/mass1.png'," \
            "anchor: new AMap.Pixel(4, 4)," \
            "size: new AMap.Size(7, 7) " \
            "},{" \
            "url: 'http://a.amap.com/jsapi_demos/static/images/mass2.png'," \
            "anchor: new AMap.Pixel(3, 3)," \
            "size: new AMap.Size(5, 5)" \
            "}]"
    amap.add_style(style)

    amap.draw('london.html')


def generate_heatmap():
    """
    [{
        "lng": 116.191031,
        "lat": 39.988585,
        "count": 10
    }, {
        "lng": 116.389275,
        "lat": 39.925818,
        "count": 11
    }, {
        "lng": 116.287444,
        "lat": 39.810742,
        "count": 12
    },...
    ]
    :return:
    """
    # step 1 地图
    amap = Heatmap(amap_key, '51.512923', '-0.113524', zoom=9)
    # step 2 读取数据
    data = pd.read_csv('london-street.csv')
    bike_data = data[data['Crime type'] == 'Bicycle theft']
    # 去掉空数据项
    bike_data_location = bike_data[bike_data['Latitude'].isnull() == False]
    bike_data_2017 = bike_data_location[
        bike_data_location['Month'] == "2017-01"]
    mass_data = []
    # step 3 将相同经纬度坐标叠加
    mass_dict = dict()
    for _, row in bike_data_2017.iterrows():
        lnglat = str(row['Longitude']) + ',' + str(row['Latitude'])
        if lnglat in mass_dict:
            mass_dict[lnglat] += 1
        else:
            mass_dict[lnglat] = 1
    for lnglat in mass_dict.keys():
        item = {"lng": float(lnglat.split(',')[0]),
                "lat": float(lnglat.split(',')[1]),
                "count": int(mass_dict[lnglat]) * 5}
        mass_data.append(item)

    amap.add_heatmap_data(mass_data)
    amap.draw('london_heatmap.html')

generate_heatmap()
