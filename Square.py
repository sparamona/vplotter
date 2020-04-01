#!/usr/bin/env python
import sys
from Plotter import Lengths,Point,Plotter



start = Point( int(sys.argv[1]), int(sys.argv[2]) )
size = Point( int(sys.argv[3]), int(sys.argv[4]) )
plotfile = open(sys.argv[5],'w')


plotarea = (250,300,942-250,650)

plotter =Plotter(plotfile)

plotter.reset()
plotter.drawLineTo( start, True )
plotter.drawLineTo( Point( start.x+size.x, start.y) , True)
plotter.drawLineTo( Point( start.x+size.x, start.y + size.y) , True)
plotter.drawLineTo( Point( start.x, start.y + size.y) , True)
plotter.drawLineTo( Point( start.x, start.y) , True)
plotter.reset()



                    
