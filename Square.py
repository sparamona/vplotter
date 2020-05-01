#!/usr/bin/env python
import sys
from Plotter import Lengths,Point,Plotter



size = Point( int(sys.argv[1]), int(sys.argv[2]) )
plotfile = open(sys.argv[3],'wb')


margins = [ 250, 100, 250, 300] # left, top, right down
totalarea = (1200, 1700)

start=Point( totalarea[0]/2-size.x/2, margins[1]+300)

plotter =Plotter(plotfile)

plotter.reset()
plotter.drawLineTo( start, False )
plotter.drawLineTo( Point( start.x+size.x, start.y) , True)
plotter.drawLineTo( Point( start.x+size.x, start.y + size.y) , True)
plotter.drawLineTo( Point( start.x, start.y + size.y) , True)
plotter.drawLineTo( Point( start.x, start.y) , True)
plotter.reset()



                    
