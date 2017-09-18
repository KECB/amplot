import math
import requests
import json
import os

from .color_dicts import MPL_COLOR_MAP, CSS4_COLORS
from .amplot import AMapPlotter


class TrackReview(AMapPlotter):

    def __init__(self, amap_key, center_lat='35.312316',
                 center_lng='102.342785', zoom=4):
        AMapPlotter.__init__(self, amap_key, center_lat, center_lng, zoom)
        self.track_path = []

    def add_track_path(self, track_path):
        self.track_path = track_path

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
            f.write('<script src="http://webapi.amap.com/ui/1.0/main.js?v=1.0'
                    '.11'
                    '"></script>')
            f.write('</head>\n')
            f.write(
                '<body>\n')
            f.write(
                '\t<div id="container"></div>\n')
            # 高德地图脚本
            f.write('<script>\n')
            # TODO 添加脚本
            self.write_map(f)
            if len(self.track_path) > 0:
                self.write_track(f)
            f.write('</script>\n')

            f.write('</body>\n')
            f.write('</html>\n')
            f.close()

    def write_track(self, f):
        f.write('AMapUI.load(["ui/misc/PathSimplifier", "lib/$"], function('
                'PathSimplifier, $) {\n')
        f.write('\tvar pathSimplifierIns = new PathSimplifier({\n')
        f.write('\t\tzIndex: 100,\n')
        f.write('\t\tmap: map, //所属的地图实例\n')
        f.write('\t\tgetPath: function(pathData, pathIndex) {\n')
        f.write('\t\t\treturn pathData.path;\n')
        f.write('\t\t},\n')
        f.write('\t\tgetHoverTitle: function(pathData, pathIndex, pointIndex) '
                '{\n')
        f.write('\t\tif (pointIndex >= 0) {\n')
        f.write('\t\t\treturn pathData.name + "，点：" + pointIndex + "/" + '
                'pathData.path.length;\n')
        f.write('\t\t}\n')
        f.write('\t\treturn pathData.name + "，点数量" + pathData.path.length;\n')
        f.write('\t\t},\n')
        f.write('\t\trenderOptions: {\n')
        f.write('\t\t\trenderAllPointsIfNumberBelow: 100 //绘制路线节点，如不需要可设置为-1\n')
        f.write('\t\t}\n')
        f.write('\t});\n')
        f.write('\twindow.pathSimplifierIns = pathSimplifierIns;\n')
        # 设置数据
        f.write('\tvar trackPath = %s\n' % json.dumps(self.track_path))
        f.write('\tpathSimplifierIns.setData([{\n')
        f.write('\t\tname: "路线0",\n')
        f.write('\t\tpath: trackPath\n')
        f.write('\t}]);\n')
        # 对第一条线路（即索引 0）创建一个巡航器
        f.write('\tvar navg1 = pathSimplifierIns.createPathNavigator(0, {\n')
        f.write('\tloop: true, //循环播放\n')
        f.write('\tspeed: 1000000 //巡航速度，单位千米/小时\n')
        f.write('\t});\n')
        f.write('\tnavg1.start();\n')
        f.write('});\n')


