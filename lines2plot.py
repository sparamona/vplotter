#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Point,Lengths,Plotter

def dash(x,y1,y2,slen):
    draw = True
    for y in range(int(y1+slen),int(y2),int(slen)):
        print "drawing to ",x,",",y, " ", draw
        v.drawLineTo(Point(x,y),draw)
        draw = not(draw)


plotfile = open(sys.argv[1],'wb')
startx = long(sys.argv[2])
v = Plotter(plotfile)
#v.drawLineTo(v.pointFromLengths(Lengths(v.W+100,v.W+100)),False)
c = (startx,200.0)
for x in range(0,100,10):
    v.drawLineTo(Point(c[0]+x,c[1]),False)
    print "starting at ", c[0]+x,",",c[1]
    dash(c[0]+x,c[1],c[1]+200.0,10)
v.reset()



print ("done.")
   
