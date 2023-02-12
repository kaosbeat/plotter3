from chiplotle3 import *
from chiplotle3.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle3.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier

import datetime
import math

plotunit = 0.025

def sign(filename,x,y):
	now = datetime.datetime.now()
	t = shapes.label(str(filename + "    " + now.strftime("%Y-%m-%d %H:%M")),0.15, 0.15, None, None, 'bottom-left')
	transforms.rotate(t, math.radians(90))
	transforms.offset(t, (x,y)) #used to be 160000
	return t


def plotgroup(g,paddingfactor,zone,noisexy,pen):
	bb = get_bounding_rectangle(g)
	bb = get_minmax_coordinates(bb.points)
	# print bb
	# plotter.select_pen(pen)
	# print (g + " is " + str(g.width*plotunit) + "mm")
	# print (g + " is " + str(g.height*plotunit) + "mm")
	# plotter.write(g)
	transforms.offset(g, (-bb[0][0] + g.width/2, -bb[0][1] + g.height/2 + 100))
	
	x1,y1 = zone[0]
	x2,y2 = zone[1]
	zw = x2 - x1
	zh = y2 - y1
	maxx = abs(x2-x1)
	maxy = abs(y2-y1)
	xfactor = maxx / g.width/paddingfactor
	yfactor = maxy / g.height/paddingfactor
	if (yfactor <= xfactor):
		scale = yfactor
		transforms.scale(g, scale)
	else:
		scale = xfactor
		transforms.scale(g, scale)
	print ("SCALE = " + str(scale))
	transforms.offset(g, (x1 - zw/2 + (zw-g.width)/2,y1 - zh/2 + (zh-g.height)/2))
	if not noisexy == (0,0):
		transforms.noise(g,noisexy)
	# plotter.write(g)
	return g

def plotgroupnew(g, zone, padding):
	# """ fit and center in zone """

	bb = get_bounding_rectangle(g)
	bb = get_minmax_coordinates(bb.points)
	print("bounding box is")
	print(bb)

	x1,y1 = zone[0]
	x2,y2 = zone[1]
	zw = x2 - x1 
	zh = y2 - y1
	zonecenter = (x1 + zw/2, y1 + zh/2)
	print (zonecenter )
	print (g.center)
	if (zh/g.height/padding < zw/g.width/padding ):
		gscale = zh/g.height/padding 
	else:
		gscale = zw/g.width/padding
	print ("scale = ", gscale)
	transforms.scale(g, gscale)
	# transforms.offset(g, (zonecenter[0] - g.center[0] - zw/2, zonecenter[1] - g.center[1] - zh/2))
	transforms.offset(g, ((zw - g.width)/2, (zh -g.height)/2))

	# l = shapes.line((g.center[0], g.center[1]),(zonecenter[0],zonecenter[1]))
	# g.append(l)
	return g 


def plotzone(zone):
	w = zone[1][0] - zone[0][0]
	h = zone[1][1] - zone[0][1]
	r = shapes.rectangle(w,h)
	transforms.offset(r,(zone[0][0] , zone[0][1]))

	return r


def addAndPlotTextmmold(x, y, size, maxsize, text):
	g = shapes.label(str(text.encode('utf-8')), size, size)
	# check https://github.com/drepetto/chiplotle/blob/master/chiplotle/hpgl/label.py
	transforms.offset(g, (x/plotunit, y/plotunit))
	if (g.width/plotunit > maxsize):
		transforms.scale(g, maxsize/(g.width/plotunit))	
	return g


def addAndPlotTextmm(size, text):
	g = shapes.label(str(text.encode('utf-8')), size, size)
	# check https://github.com/drepetto/chiplotle/blob/master/chiplotle/hpgl/label.py
	# transforms.offset(g, (x/plotunit, y/plotunit))
	# if (g.width/plotunit > maxsize):
	#     transforms.scale(g, maxsize/(g.width/plotunit))	
	return g
def calculatesvggroup(svg):
	print ("PLOTTING stuff")
	# plotter.select_pen(pen)
	g = shapes.group([])
	paths, attributes = svg2paths(svg)
	# print dir(paths[0][0].start.real)
	for path in paths:
		for segment in path:
			if isinstance(segment, Line):
				# print "Line found"
				g.append(shapes.line((segment.start.real,segment.start.imag),(segment.end.real,segment.end.imag)))
			if isinstance(segment, CubicBezier):
				g.append(shapes.bezier_path([(segment.start.real,segment.start.imag),(segment.control1.real,segment.control1.imag),(segment.control2.real,segment.control2.imag),(segment.end.real,segment.end.imag)],0))
	bb = get__rectangle(g)
	bb = get_minmax_coordinates(bb.points)
	print (bb)
	print (svg + " is " + str(g.width*plotunit) + "mm")
	print (svg + " is " + str(g.height*plotunit) + "mm")
	# plotter.write(g)
	transforms.offset(g, (-bb[0][0], -bb[0][1] ))
	return({'group': g, 'bounds': bb})
	# io.view(g)




def plotSVG(plotter,zone,file):
	x,y = zone[0]
	width = zone[1][0] - zone[0][0]
	height = zone[1][1] - zone[0][1]
	svg = file.encode('utf-8')
	### colors represent PENS
	# black RGB(0,0,0) = pen1
	# red RGB(255,0,0) = pen2
	# blue RGB(0,0,255) = pen3
	# from blender use 		if stroke == 'rgb(0, 119, 0)'    format
	# from inkscape use        if stroke == '#000000':       format
	# after scour optimize use  if stroke == '#000':       format for primary RGB colors!
	#pipeSVG through SCOUR to fix attributes!

	f = shapes.group([])
	g = shapes.group([])
	h = shapes.group([])
	paths, attributes = svg2paths(svg)
	for idx, path in enumerate(paths):
		# print('\n')
		# print(idx)
		# print attributes[idx]['style']['stroke']
		stroke = attributes[idx]['stroke']
		layer = f
		if stroke == '#000000': 
			layer = f
		if stroke == '#000': 
			layer = f
		if stroke == 'rgb(0, 0, 0)': 
			layer = f
		if stroke == '#f00': 
			layer = g
		if stroke == '#ff0000': 
			layer = g
		if stroke == 'rgb(255, 0, 0)': 
			layer = g
		if stroke == '#00f': 
			layer = h
		if stroke == '#0000ff': 
			layer = h
		if stroke == 'rgb(0, 0, 255)': 
			layer = h    
		p = []
		# print(path)
		if isinstance(path[0], Line):
			# print("Line instance found", path[0])
			p.append((path[0].start.real,path[0].start.imag))
			pathtype = "line"
		if isinstance(path[0], QuadraticBezier):
			# print("insta111nce found")
			#print(path)
			pathtype = "qbezier"
			p.append((path[0].start.real,path[0].start.imag))
		if isinstance(path[0], CubicBezier):
			# print("insta111nce found")
			#print(path)
			pathtype = "cbezier"
			p.append((path[0].start.real,path[0].start.imag))
		for segment in path:
			if isinstance(segment, Line):
				p.append((segment.end.real,segment.end.imag))
				#print('still appending lines')
			#	layer.append(shapes.line((segment.start.real,segment.start.imag),(segment.end.real,segment.end.imag)))
			if isinstance(segment, QuadraticBezier):
				#print("Bezier found")
				# p.append(shapes.bezier_path([(segment.start.real,segment.start.imag),(segment.control1.real,segment.control1.imag),(segment.control2.real,segment.control2.imag),(segment.end.real,segment.end.imag)],0))
				p.append((segment.control.real,segment.control.imag))
				p.append((segment.end.real,segment.end.imag))
			if isinstance(segment, CubicBezier):
				#print("Bezier found")
				# p.append(shapes.bezier_path([(segment.start.real,segment.start.imag),(segment.control1.real,segment.control1.imag),(segment.control2.real,segment.control2.imag),(segment.end.real,segment.end.imag)],0))
				p.append((segment.control1.real,segment.control1.imag))
				p.append((segment.end.real,segment.end.imag))
		if (pathtype == 'line'):
			layer.append(shapes.path(p))
		else:
			layer.append(shapes.bezier_path(p,0.5))
	# print(f.width,g.width,h.width)
	bb1 = get_bounding_rectangle(f)
	bb2 = get_bounding_rectangle(g)
	bb3 = get_bounding_rectangle(h)
	bb = shapes.group([]) 
	## merge al bounding boxes to get total outline
	bb.append(bb1)
	bb.append(bb2)
	bb.append(bb3)
	bb = get_bounding_rectangle(bb)
	bb = get_minmax_coordinates(bb.points)
	# print (bb)
	# print (svg + " is " + str(bb[1]) + "mm")
	# print (svg + " is " + str(bb[0]) + "mm")
	# plotter.write(g)
	transforms.offset(f, (-bb[0][0], -bb[0][1] ))
	transforms.offset(g, (-bb[0][0], -bb[0][1] ))
	transforms.offset(h, (-bb[0][0], -bb[0][1] ))
	#scale to fullsize
	totalwidth = bb[1][0] - bb[0][0]
	totalheight = bb[1][1] - bb[0][1]
	print (totalwidth)
	# if (w/totalwidth < 1):
	if (height/totalheight < width/totalwidth):
		print("heights")
		print (height)
		print(totalheight)
		scale = height/totalheight
	else:
		scale = width/totalwidth

	# print(g)
	# if len(h) > 0:
	# 	sc = min( [15000/g.width, 15000/h.width, 10000/g.height, 10000/h.height])
	# else:
	# 	sc = min([15000/g.width, 10000/g.height])
	# print (sc)
	transforms.rotate(f, math.radians(180))
	transforms.rotate(g, math.radians(180))
	transforms.rotate(h, math.radians(180))
	transforms.scale(f, scale)
	transforms.scale(g, scale)
	transforms.scale(h, scale)
	transforms.offset(f, (x + width,y + height))
	transforms.offset(g, (x + width,y + height))
	transforms.offset(h, (x + width,y + height))
	#get the bb again after transformation/scale/offset
	bb1 = get_bounding_rectangle(f)
	bb2 = get_bounding_rectangle(g)
	bb3 = get_bounding_rectangle(h)
	bb = shapes.group([]) 
	## merge al bounding boxes to get total outline
	bb.append(bb1)
	bb.append(bb2)
	bb.append(bb3)
	bb = get_bounding_rectangle(bb)
	bb = get_minmax_coordinates(bb.points)
	#io.view(g)
	# print ("de groepen", len(g), len(h))
	return({'groups': [f,g,h], 'bounds': bb})