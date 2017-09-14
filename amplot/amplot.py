import math
import requests
import json
import os

from .color_dicts import MPL_COLOR_MAP, CSS4_COLORS


def safe_iter(var):
    try:
        return iter(var)
    except TypeError:
        return [var]


class AMapPlotter(object):
    def __init__(self, amap_key, center_lat, center_lng, zoom):
        """
        
        :param amap_key: 必填, 高德地图 API_KEY, 用于调用 REST_API
        :param center_lat: 
        :param center_lng: 
        :param zoom: 
        """
        self.key = amap_key
        self.center = (float(center_lat), float(center_lng))
        self.zoom = int(zoom)
        self.grids = None
        self.paths = {}
        self.shapes = {}
        self.circles = {}
        self.points = []
        self.heatmap_points = []
        self.radpoints = []
        self.gridsetting = None
        self.color_icon = os.path.join(os.path.dirname(__file__),
                                       'markers/%s.png')
        self.color_dict = MPL_COLOR_MAP
        self.html_color_codes = CSS4_COLORS
        self.__counter = 0

    def from_geocode(self, location_string, zoom=13):
        lat, lng = self.geocode(location_string)
        return lat, lng, zoom

    def geocode(self, location_string):
        geocode = requests.get(
            'http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s' % (
                self.key, location_string))
        geocode = json.loads(geocode.text, encoding='utf-8')
        lng, lat = geocode['geocodes'][0]['location'].split(',')
        return lat, lng

    def grid(self, slat, elat, latin, slng, elng, lngin):
        self.gridsetting = [slat, elat, latin, slng, elng, lngin]

    def marker(self, lat, lng, color='#FF0000', title='no implementation'):
        color = self.color_dict.get(color, color)
        color = self.html_color_codes.get(color, color)
        self.points.append(lat, lng, color[1:], title)

    def scatter(self, lats, lngs, color=None, size=40, marker=True, **kwargs):
        size = size or 40
        kwargs["color"] = color
        kwargs["size"] = size
        settings = self._process_kwargs(kwargs)
        for lat, lng in zip(lats, lngs):
            if marker:
                self.marker(lat, lng, settings['color'])
            else:
                self.circle(lat, lng, size, **settings)

    def circle(self, lat, lng, radius, name=None, color=None, **kwargs):
        kwargs.setdefault('face_alpha', 0.5)
        kwargs.setdefault('face_color', "#000000")
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        if not name:
            self.__counter += 1
            name = 'circle' + str(self.__counter)
        self.circles[name] = {'lat': lat, 'lng': lng, 'radius': radius,
                              'settings': settings}

    def get_cycle(self, lat, lng, rad):
        # unit of radius: meter
        cycle = []
        d = (rad / 1000.0) / 6378.8
        lat1 = (math.pi / 180.0) * lat
        lng1 = (math.pi / 180.0) * lng

        r = [x * 10 for x in range(36)]
        for a in r:
            tc = (math.pi / 180.0) * a
            y = math.asin(
                math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(
                    d) * math.cos(tc))
            dlng = math.atan2(math.sin(
                tc) * math.sin(d) * math.cos(lat1),
                              math.cos(d) - math.sin(lat1) * math.sin(y))
            x = ((lng1 - dlng + math.pi) % (2.0 * math.pi)) - math.pi
            cycle.append(
                (float(y * (180.0 / math.pi)), float(x * (180.0 / math.pi))))
        return cycle

    def add_path(self, points, name=None, color=None, **kwargs):
        """
        添加路径/线
        :param points: type is list, eg.  [[116.368904, 39.913423],
                                           [116.382122, 39.901176],
                                           [116.387271, 39.912501],
                                           [116.398258, 39.904600]]
        :param name: 路径名称, 如果不定义, uuid生成
        :param color:
        :param kwargs:
        """
        kwargs.setdefault('color', color)
        settings = self._process_kwargs(kwargs)
        if not name:
            self.__counter += 1
            name = 'path' + str(self.__counter)
        self.paths[name] = {'path': points, 'settings': settings}

    def add_polygon(self, points, name=None, color=None, **kwargs):
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        if not name:
            self.__counter += 1
            name = 'polygon' + str(self.__counter)
        self.shapes[name] = {'path': points, 'settings': settings}

    def heatmap(self, lats, lngs, threshold=10, radius=10, gradient=None, opacity=0.6, dissipating=True):
        """
        :param lats: list of latitudes
        :param lngs: list of longitudes
        :param threshold:
        :param radius: The hardest param. Example (string):
        :return:
        """
        settings = {}
        settings['threshold'] = threshold
        settings['radius'] = radius
        settings['gradient'] = gradient
        settings['opacity'] = opacity
        settings['dissipating'] = dissipating
        settings = self._process_heatmap_kwargs(settings)

        heatmap_points = []
        for lat, lng in zip(lats, lngs):
            heatmap_points.append((lat, lng))
        self.heatmap_points.append((heatmap_points, settings))

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
            self.write_paths(f)
            self.write_shapes(f)
            self.write_circles(f)
            f.write('</script>\n')

            f.write('</body>\n')
            f.write('</html>\n')
            f.close()

    def _process_heatmap_kwargs(self, settings_dict):
        settings_string = ''
        settings_string += "heatmap.set('threshold', %d);\n" % settings_dict['threshold']
        settings_string += "heatmap.set('radius', %d);\n" % settings_dict['radius']
        settings_string += "heatmap.set('opacity', %f);\n" % settings_dict['opacity']

        dissipation_string = 'true' if settings_dict['dissipating'] else 'false'
        settings_string += "heatmap.set('dissipating', %s);\n" % (dissipation_string)

        gradient = settings_dict['gradient']
        if gradient:
            gradient_string = "var gradient = [\n"
            for r, g, b, a in gradient:
                gradient_string += "\t" + "'rgba(%d, %d, %d, %d)',\n" % (r, g, b, a)
            gradient_string += '];' + '\n'
            gradient_string += "heatmap.set('gradient', gradient);\n"

            settings_string += gradient_string

        return settings_string

    def _process_kwargs(self, kwargs):
        settings = dict()
        settings["edge_color"] = kwargs.get("color", None) or \
                                 kwargs.get("edge_color", None) or \
                                 kwargs.get("ec", None) or "#000000"

        settings["edge_alpha"] = kwargs.get("alpha", None) or \
                                 kwargs.get("edge_alpha", None) or \
                                 kwargs.get("ea", None) or \
                                 kwargs.get("opacity", None) or \
                                 1.0

        settings["fill_opacity"] = kwargs.get("fill_opacity", None) or 1.0
        settings["fill_color"] = kwargs.get("fill_color", None) or "#000000"
        # TODO 用更习惯的命名方式
        settings["edge_width"] = kwargs.get("edge_width", None) or \
                                 kwargs.get("ew", None) or \
                                 1.0
        settings["face_alpha"] = kwargs.get("alpha", None) or \
                                 kwargs.get("face_alpha", None) or \
                                 kwargs.get("fa", None) or \
                                 0.3
        settings["face_color"] = kwargs.get("color", None) or \
                                 kwargs.get("face_color", None) or \
                                 kwargs.get("fc", None) or \
                                 "#000000"

        settings["color"] = kwargs.get("color", None) or \
                            kwargs.get("c", None) or \
                            settings["edge_color"] or \
                            settings["face_color"]

        # Need to replace "plum" with "#DDA0DD" and "c" with "#00FFFF" (cyan).
        for key, color in settings.items():
            if 'color' in key:
                color = self.color_dict.get(color, color)
                color = self.html_color_codes.get(color, color)
                settings[key] = color

        settings["closed"] = kwargs.get("closed", None)

        return settings

    def write_map(self, f):
        f.write('\tvar map = new AMap.Map("container", {\n')
        f.write('\t\tresizeEnable: true,\n')
        f.write('\t\tcenter: [%f, %f],\n' % (self.center[1], self.center[0]))
        f.write('\t\tzoom: %d\n' % self.zoom)
        f.write('\t});\n')

    def write_paths(self, f):
        for name, path in self.paths.items():
            self.write_polyline(f, name, path)

    def write_shapes(self, f):
        for name, path in self.shapes.items():
            self.write_polygon(f, name, path)

    def write_circles(self, f):
        for name, settings in self.circles.items():
            self.write_circle(f, name, settings)

    def write_polyline(self, f, name, path):
        settings = path['settings']
        line = path['path']
        stroke_color = settings.get('color') or settings.get('edge_color')
        stroke_opacity = settings.get('edge_alpha')
        stroke_weight = settings.get('edge_width')

        # 转换成 string
        line = json.dumps(line)
        f.write('var %sArr = %s;\n' % (name, line))

        f.write('var %s = new AMap.Polyline({\n' % name)
        f.write('\tpath:%sArr,\n' % name)
        f.write('\tstrokeColor:"%s",\n' % stroke_color)
        f.write('\tstrokeOpacity:%s,\n' % stroke_opacity)
        f.write('\tstrokeWeight:%s,\n' % stroke_weight)
        # TODO 提取线样式
        f.write('\tstrokeStyle:"%s",\n' % 'solid')
        f.write('\tstrokeDasharray: [10, 5] // 补充线样式\n')
        f.write('});')
        f.write('\n')

        f.write('%s.setMap(map);\n' % name)
        f.write('\n\n')

    def write_polygon(self, f, name, path):
        settings = path['settings']
        lines = path['path']
        stroke_color = settings.get('color') or settings.get('edge_color')
        stroke_opacity = settings.get('edge_alpha')
        stroke_weight = settings.get('edge_width')
        fill_color = settings.get('fill_color')
        fill_opacity = settings.get('fill_opacity')

        #  转成 string
        lines = json.dumps(lines)
        f.write('var %sArr = %s\n;' % (name, lines))

        f.write('var %s = new AMap.Polygon({\n' % name)
        f.write('\tpath:%sArr,\n' % name)
        f.write('\tstrokeColor:"%s",\n' % stroke_color)
        f.write('\tstrokeOpacity:%s,\n' % stroke_opacity)
        f.write('\tstrokeWeight:%s,\n' % stroke_weight)
        f.write('\tfillColor:"%s",\n' % fill_color)
        f.write('\tfillOpacity: %s\n' % fill_opacity)
        f.write('});')
        f.write('\n')

        f.write('%s.setMap(map);\n' % name)
        f.write('\n\n')

    def write_circle(self, f, name, settings):
        lat, lng, radius = settings.get('lat'), settings.get('lng'), \
                           settings.get('radius')
        settings = settings['settings']
        stroke_color = settings.get('color') or settings.get('edge_color')
        stroke_opacity = settings.get('edge_alpha')
        stroke_weight = settings.get('edge_width')
        fill_color = settings.get('fill_color')
        fill_opacity = settings.get('fill_opacity')

        f.write('var %s = new AMap.Circle({\n' % name)
        f.write('\tcenter: new AMap.LngLat("%s", "%s"),\n' % (lng, lat))
        f.write('\tradius:%s,\n' % radius)
        f.write('\tstrokeColor:"%s",\n' % stroke_color)
        f.write('\tstrokeOpacity:%s,\n' % stroke_opacity)
        f.write('\tstrokeWeight:%s,\n' % stroke_weight)
        f.write('\tfillColor:"%s",\n' % fill_color)
        f.write('\tfillOpacity: %s\n' % fill_opacity)
        f.write('});')
        f.write('\n')

        f.write('%s.setMap(map);\n' % name)
        f.write('\n\n')