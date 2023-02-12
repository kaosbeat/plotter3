from copy import deepcopy
from chiplotle3 import *
from PIL import Image
import sys
from lib.texttools  import plotfilledchar,writeword,plotchar
from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
from chiplotle3.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle3.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from lib.plothelpers import sign
from lib.recaptcha import recaptcha
from lib.tweetplot import TweetImgTxt, convertSVGtoTweet
import time 
filename = sys.argv[1]
virtualplotting = sys.argv[2]
tweetit = False
#print(virtualplotting)
if (virtualplotting == 'virtual'):
        plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
        plotter = instantiate_plotters()[0]
        print("plotting for real")

# plotter.margins.hard.draw_outline()
# plotter = instantiate_plotters( )[0]
# real plotter says
#    Drawing limits: (left 0; bottom 0; right 16158; top 11040)
plotunit = 0.025
pltmax = [16158, 11040]
A3mm = [420,297]  
A3 = [A3mm[0]/plotunit, A3mm[1]/plotunit] # 16800, 11880  is bigger than pltmax!!
paper = shapes.rectangle(pltmax[0], pltmax[1])
transforms.offset(paper,(pltmax[0]/2,pltmax[1]/2))
plotter.select_pen(2)
plotter.write(paper)
#coords = plotter.margins.soft.all_coordinates
# plotter.select_pen(1)
b = 0

# viewport = (10320,7920)
# horizon = (viewport[0] / 2, viewport[1] / 2)

import math
import random
import numpy as np
from scipy import signal
# from texttools  import *
import freetype

from PIL import Image
im = Image.open('text.png')
w,h = im.size
print(im.size)

pixels = list(im.getdata())
xcur = 0
scanlines = []
g = shapes.group([])
for y in range(h):
    scanlines.append([])
    for x in range(w):
        el = pixels[(y*w)+x][0]
        if el != 0:
            el = 1
        scanlines[y].append(el)
# print(pixels[0])
# print(scanlines)
drawlines = []
for scanline in scanlines:
    done = False
    nxt = 0
    cur = 0
    indexer = 1
    drawline = []
    if scanline[0] == 1:
        indexer = 0
    if indexer != 0: # flip this to invert
        drawline.append(nxt)
    while done == False:
        # print(nxt)
        try:
            nxt = scanline[cur:-1].index(indexer)
            cur = cur + nxt
        except ValueError:
            cur = w
        drawline.append(cur)
        if cur == w:
            done = True
        if indexer == 1:
            indexer = 0
        else:
            indexer = 1
        # time.sleep(0.1)
    # print (drawline)
    drawlines.append(drawline)


for y,drawline in enumerate(drawlines):
    size = random.randint(0,1)+30
   
    if drawline[0] == 0:
        black = True
    for i in range(len(drawline)-1):
        if black:
            jitter = random.randint(0,size)-size/2
            g.append(shapes.line((drawline[i]*size,-y*size + jitter),(drawline[i+1]*size,-y*size + jitter)))
            black = False
        else:
            black = True
        

print (g.width, g.height)
scx = pltmax[0]/g.width
scy = pltmax[1]/g.height
sc = min(scx,scy)
transforms.scale(g, sc)
transforms.center_at(g,(pltmax[0]/2, pltmax[1]/2))
plotter.write(g)
io.view(plotter)
            



