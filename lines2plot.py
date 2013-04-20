#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Point,Lengths,Plotter


plotfile = open(sys.argv[1],'wb')

v = Plotter(plotfile)
#v.drawLineTo(v.pointFromLengths(Lengths(v.W+100,v.W+100)),False)
v.drawLineTo(Point(300.0,500.0),False)
v.drawLineTo(Point(700.0,500.0),True)
v.drawLineTo(Point(700.0,400.0),True)
v.drawLineTo(Point(300.0,400.0),True)
v.drawLineTo(Point(300.0,500.0),True)
v.reset()

print ("done.")
   
