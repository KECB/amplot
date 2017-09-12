from amplot import AMapPlotter

with open('key', 'r') as f:
    key = f.readline()
amap_key = key
amap = AMapPlotter(amap_key, '39.90923', '116.397428', 13)
amap.geocode('中大科技园')
# lines = [[116.368904, 39.913423],
#          [116.382122, 39.901176],
#          [116.387271, 39.912501],
#          [116.398258, 39.904600]]
lats = []
lngs = []
# for points in lines:
#     lats.append(points[1])
#     lngs.append(points[0])
# amap.plot(lats, lngs, color='blue', edge_width='5')

shape = [[116.403322, 39.920255],
         [116.410703, 39.897555],
         [116.402292, 39.892353],
         [116.389846, 39.891365]]
for points in shape:
    lats.append(points[1])
    lngs.append(points[0])
amap.polygon(lats, lngs, color='cyan', opacity='0.2', fill_color='firebrick',
             fill_opacity='0.35')
amap.draw('test.html')
