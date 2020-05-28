#!/usr/bin/env python
import sys
from Plotter import Lengths,Point,Plotter
from math import sin,cos,pi,radians


radius = int(sys.argv[1])
#center = Point(int(sys.args[2]), int(sys.args[3]))
plotfile = open(sys.argv[2],'wb')


margins = [ 250, 100, 250, 300] # left, top, right down
totalarea = (1200, 1700)

plotter =Plotter(plotfile)
origin = plotter.pointFromLengths(plotter.currentLengths)
#start = Point(origin.x-size.x/2,origin.y+20)
start = Point(origin.x,origin.y+100)

plotter.reset()

def circlePoint(center,theta, r):
    return Point(center.x+r*cos(theta),center.y+r*sin(theta))


plotter.drawLineTo( circlePoint(start,0, radius), False)
for degs in range(0,360):
    plotter.drawLineTo( circlePoint(start,radians(degs), radius),True)

plotter.reset()





                    
