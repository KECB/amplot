from amplot import AMapPlotter
from amplot import MassPlotter
from amplot import Heatmap
import requests
import json

def basics():
    """
    测试画圆, 画线, 画多边形.
    """
    with open('key', 'r') as f:
        key = f.readline()
    amap_key = key
    # 设定地图中心, 地图放大 level
    amap = AMapPlotter(amap_key, '39.90923', '116.397428', 13)
    # 获取经纬度
    amap.geocode('中大科技园')

    # 第一条线坐标集合
    lines = [[116.368904, 39.913423],
             [116.382122, 39.901176],
             [116.387271, 39.912501],
             [116.398258, 39.904600]]
    amap.add_path(lines, color='blue', edge_width='5')
    # 第二条线坐标集合
    lines = [[116.388904, 39.913423],
             [116.372122, 39.901176],
             [116.367271, 39.912501],
             [116.358258, 39.904600]]
    amap.add_path(lines,name='secondline', color='mediumseagreen', \
                                                edge_width='5')

    # 第一多边形坐标集合
    shape = [[116.403322, 39.920255],
             [116.410703, 39.897555],
             [116.402292, 39.892353],
             [116.389846, 39.891365]]
    amap.add_polygon(shape, color='cyan', opacity='0.2', fill_color='firebrick',
                     fill_opacity='0.35')
    # 第二多边形坐标集合
    shape = [[116.409322, 39.920255],
             [116.413703, 39.897555],
             [116.405292, 39.892353],
             [116.383846, 39.891365]]
    amap.add_polygon(shape, name='second', color='cyan', opacity='0.2',
                     fill_color='firebrick',
                     fill_opacity='0.35')
    # 第一圆心坐标及圆大小
    amap.circle(39.920255, 116.403322, 1000, color='red', opacity='1',
                fill_color='red', fill_opacity='0.35')
    # 第二圆心坐标及圆大小
    amap.circle(39.920255, 116.403322, 500, color='red', opacity='1',
                fill_color='red', fill_opacity='0.35')
    # 第三圆心坐标及圆大小
    amap.circle(39.159556, -94.337896, 10000, color='red', opacity='1',
                fill_color='red', fill_opacity='0.35')
    # 生成 html
    amap.draw('test.html')


def mass_marker():
    """
        测试画圆, 画线, 画多边形.
        """
    with open('key', 'r') as f:
        key = f.readline()
    amap_key = key
    amap = MassPlotter(amap_key, '35.312316', '102.342785', 4)
    # step1 加载海量数据
    response = requests.get('http://a.amap.com/jsapi_demos/static/citys.js')
    data = json.loads(response.text.split('=')[1])
    amap.add_mass_marker(data)
    # step2 为数据增加样式属性
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
    # step3 生成 html
    amap.draw('mass.html')


def heatmap():
    """
        测试画圆, 画线, 画多边形.
        """
    with open('key', 'r') as f:
        key = f.readline()
    amap_key = key
    amap = Heatmap(amap_key, '39.921984', '116.418261', 11)
    # step1 加载热度地图数据
    response = requests.get(
                'http://a.amap.com/jsapi_demos/static/resource/heatmapData.js')
    response = response.text.replace('\n','').replace(' ','')
    data = json.loads(response.split('=')[1][:-1])
    amap.add_heatmap_data(data)

    # step2 生成 html
    amap.draw('heatmap.html')


heatmap()
