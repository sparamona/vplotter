#!/usr/bin/env python
import sys
from Plotter import Lengths,Point,Plotter



size = Point( int(sys.argv[1]), int(sys.argv[2]) )
plotfile = open(sys.argv[3],'wb')


margins = [ 250, 100, 250, 300] # left, top, right down
totalarea = (1200, 1700)

plotter =Plotter(plotfile)
origin = plotter.pointFromLengths(plotter.currentLengths)
start = Point(origin.x-size.x/2,origin.y+20)

plotter.reset()
plotter.drawLineTo( start, False )
plotter.drawLineTo( Point( start.x+size.x, start.y) , True)
plotter.drawLineTo( Point( start.x+size.x, start.y + size.y) , True)
plotter.drawLineTo( Point( start.x, start.y + size.y) , True)
plotter.drawLineTo( Point( start.x, start.y) , True)
plotter.reset()

    


                    
