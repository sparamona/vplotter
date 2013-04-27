#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Point,Lengths,Plotter


plotfile = open(sys.argv[1],'wb')

v = Plotter(plotfile)
#v.drawLineTo(v.pointFromLengths(Lengths(v.W+100,v.W+100)),False)
c = (550.0,380.0)
for i in range(20,1,-2):
    v.drawLineTo(Point(c[0]-i,c[1]-i),False)
    v.drawLineTo(Point(c[0]-i,c[1]+i),True)
    v.drawLineTo(Point(c[0]+i,c[1]+i),True)
    v.drawLineTo(Point(c[0]+i,c[1]-i),True)
    v.drawLineTo(Point(c[0]-i,c[1]-i),True)
v.reset()

print ("done.")
   
