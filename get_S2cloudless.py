"""
Modified on Tue 29 May 2018
@author: Kamieljv (GitHub)
Source: modified from Ahmet Taspinar (http://ataspinar.com/2017/12/04/using-convolutional-neural-networks-to-detect-features-in-sattelite-images/)
get_S2cloudless.py:
    download map tiles from Sentinel-2 cloudless
    write map tiles to folder
"""

from owslib.wms import WebMapService
import os.path
from PIL import Image

URL = "https://tiles.maps.eox.at/wms?service=wms&request=getcapabilities"
wms = WebMapService(URL, version='1.1.1')

OUTPUT_DIRECTORY = '' #fill in output directory for the images

#DEFINING GRID, going from top left to bottom right
x_min = 0 #fill in minimum x-coordinate
y_max = 1 #fill in minimum y-coordinate
dx, dy = 0.0125, 0.0125 #fill in the dimensions of the tiles (in latlong degrees)
no_tiles_x = 5 #fill in number of tiles in x-direction
no_tiles_y = 5 #fill in number of tiles in y-direction
total_no_tiles = no_tiles_x * no_tiles_y
print('Total tiles: {}'.format(total_no_tiles))

x_max = x_min + no_tiles_x * dx
y_min = y_max - no_tiles_y * dy
BOUNDING_BOX = [x_min, y_min, x_max, y_max]
print('Bbox: ', BOUNDING_BOX)

#Make requests in a loop
for jj in range(0,no_tiles_y):
    for ii in range(0,no_tiles_x):
        bid = ii + no_tiles_x*jj
        if bid%1000==0:
            print("Progress: "+str(round(bid/total_no_tiles*100,2))+' %')
        bid = '%06d' % bid
        ll_x_ = x_min + ii*dx
        ll_y_ = y_max - jj*dy
        bbox = (ll_x_, ll_y_ - dy, ll_x_ + dx, ll_y_)
        filename = "{}_{}_{}_{}_{}.jpg".format(bid, round(bbox[0],3), round(bbox[1],3), round(bbox[2],3), round(bbox[3],3))
        if not os.path.isfile(OUTPUT_DIRECTORY+filename):
            img = wms.getmap(layers=['s2cloudless'],srs='EPSG:4326', bbox=bbox, size=(256, 256), format='image/jpeg', transparent=True)
            out = open(OUTPUT_DIRECTORY + filename, 'wb')
            out.write(img.read())
            out.close()