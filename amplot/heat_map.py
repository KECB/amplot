import math
import requests
import json
import os

from .color_dicts import MPL_COLOR_MAP, CSS4_COLORS
from .amplot import AMapPlotter


class Heatmap(AMapPlotter):

    def __init__(self, amap_key, center_lat='35.312316',
                 center_lng='102.342785', zoom=4):
        AMapPlotter.__init__(self, amap_key, center_lat, center_lng, zoom)
        self.heatmap_data = []
        self.style = ''

    def add_heatmap_data(self, data):
        self.heatmap_data = data

    def add_style(self, marker_style):
        self.style = marker_style

    def draw(self, htmlfile, title='高德地图演示'):
        with open(htmlfile, 'w') as f:
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('<meta charset="utf-8">\n')
            f.write('<meta http-equiv="X-UA-Compatible" content="IE=edge">\n')
            f.write('<meta name="viewport" content="initial-scale=1.0, '
                    'user-scalable=no, width=device-width">\n')
            f.write('<title>%s</title>\n' % title)
            f.write('<link rel="stylesheet" '
                    'href="http://cache.amap.com/lbs/static/main1119.css"/>\n')
            f.write('<script '
                    'src="http://webapi.amap.com/maps?v=1.3&key=%s"></script'
                    '>\n' % self.key)
            f.write('<script type="text/javascript" '
                    'src="http://cache.amap.com/lbs/static/addToolbar.js'
                    '"></script>\n')
            f.write('</head>\n')
            f.write(
                '<body>\n')
            f.write(
                '\t<div id="container"></div>\n')
            # 高德地图脚本
            f.write('<script>\n')
            # TODO 添加脚本
            self.write_map(f)
            if len(self.heatmap_data) > 0:
                self.write_heatmap(f)
            f.write('</script>\n')

            f.write('</body>\n')
            f.write('</html>\n')
            f.close()


    def write_heatmap(self, f):
        """
        详细的参数,可以查看heatmap.js的文档 http://www.patrick-wied.at/static/heatmapjs/docs.html
        参数说明如下:
         * visible 热力图是否显示,默认为true
         * opacity 热力图的透明度,分别对应heatmap.js的minOpacity和maxOpacity
         * radius 势力图的每个点的半径大小
         * gradient  {JSON} 热力图的渐变区间 . gradient如下所示
         *	{
         .2:'rgb(0, 255, 255)',
         .5:'rgb(0, 110, 255)',
         .8:'rgb(100, 0, 255)'
         }
         其中 key 表示插值的位置, 0-1
         value 为颜色值
        """
        # 判断是否支持 canvas
        f.write('var elem = document.createElement("canvas");\n')
        f.write('var isSupport=!!(elem.getContext && elem.getContext("2d"));\n')
        f.write('if (!isSupport){\n')
        f.write('\talert("热力图仅对支持canvas的浏览器适用,您所使用的浏览器不能使用热力图功能,请换个浏览器试试~")\n')
        f.write('}\n')
        # 加载插件
        f.write('var heatmap;\n')
        f.write('map.plugin(["AMap.Heatmap"], function() {\n')
        # 初始化heatmap对象
        f.write('\theatmap = new AMap.Heatmap(map, {\n')
        # TODO 自定义给定半径
        f.write('\t\tradius: 25, //给定半径\n')
        f.write('\t\topacity: [0, 0.8]\n')
        f.write('\t});\n')
        # 设置数据集
        f.write('var heatmapData=%s;\n' % json.dumps(self.heatmap_data))
        f.write('\theatmap.setDataSet({\n')
        f.write('\t\tdata: heatmapData,\n')
        f.write('\t\tmax: 100\n')
        f.write('\t});\n')
        f.write('});\n')



