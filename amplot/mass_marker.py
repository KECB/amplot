import math
import requests
import json
import os

from .color_dicts import MPL_COLOR_MAP, CSS4_COLORS
from .amplot import AMapPlotter


class MassPlotter(AMapPlotter):

    def __init__(self, amap_key, center_lat, center_lng, zoom):
        AMapPlotter.__init__(self, amap_key, center_lat, center_lng, zoom)
        self.mass_marker = []
        self.style = ''

    def add_mass_marker(self, mass_marker):
        self.mass_marker = mass_marker

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
            self.write_style(f)
            self.write_mass(f)
            f.write('</script>\n')

            f.write('</body>\n')
            f.write('</html>\n')
            f.close()

    def write_style(self, f):
        f.write('var style=%s;\n' % self.style)

    def write_mass(self, f):
        f.write('var massData = %s\n' % json.dumps(self.mass_marker))
        f.write('var mass = new AMap.MassMarks(massData, {\n')
        # TODO 参数可传递
        f.write('\topacity: 0.8,\n')
        f.write('\tzIndex:111,\n')
        f.write('\tcursor:"pointer",\n')
        f.write('\tstyle:style\n')
        f.write('});\n')
        f.write('mass.setMap(map);\n')


