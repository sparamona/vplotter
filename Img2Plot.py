#!/usr/bin/env python
import sys,collections,gc,time,Image
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Lengths,Point,Plotter

def inbox(p,box):
    return (p.x>=box[0]) and (p.x<=box[2]) and (p.y>=box[1]) and (p.y<=box[3])


class MODES:
    left=0
    right=1
    top=2

class Img2Plot(Plotter):

    def __init__(self,sourcefile,plotfile):
        Plotter.__init__(self,plotfile)
        self.im = Image.open(sourcefile)

   
    def sweep(self, mode, offset, bbox, plotarea, direction, rgb, vrange):
       if mode==MODES.top:
           r=range(bbox[0],bbox[2],5)
       elif (mode==MODES.left) or (mode==MODES.right):
           r=range(bbox[1]+5,bbox[3],15)

       for i in r:
            sys.stdout.write('.')
            sys.stdout.flush()
            if mode==MODES.top:
                movetop = Point(i,offset.y+1)
            elif mode==MODES.left:
                movetop = Point(offset.x+1,i)
            elif mode==MODES.right:
                movetop = Point(bbox[2]-1,i)
            self.moveTo(self.lengthsFromPoint(movetop))
            l = self.currentLengths
            state = 0
            while True:
                # now add keep adding steps, and use penup/pendown
                l=Lengths(l.a+direction[0]*self.stepLength,l.b+direction[1]*self.stepLength)
                p = self.pointFromLengths(l)
                #print "at point ",p
                if state==2 or (inbox(p,plotarea)==False):
                    break
                try: 
                    if inbox(p,bbox):
                        pix = self.im.getpixel((p.x-offset.x,p.y-offset.y))
                        pencommand = 2 if (pix[rgb]>vrange[0] and pix[rgb]<=vrange[1]) else 1
                        state = 1
                    else:
                        pencommand=1
                        if state==1:
                            state=2
                    b = (direction[0]<<4) + (direction[1]<<2) +  pencommand
                    self.plotfile.write(chr(b))
                    self.currentLengths=l
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
    

        

    def draw(self):

        # fix b first
        margin = 200
        offset = Point(200,200)
        plotarea = (margin,margin,self.W-margin,self.W-margin)

        bbox = (max(plotarea[0],offset.x),
                max(plotarea[1],offset.y),
                min(plotarea[2],self.im.getbbox()[2]+offset.x),
                min(plotarea[3],self.im.getbbox()[3]+offset.y))
        print bbox

        self.sweep(MODES.top, offset,bbox, plotarea, (1,1),0,(0,70))
        self.sweep(MODES.top, offset,bbox, plotarea, (1,0),1,(0,140))
        self.sweep(MODES.left, offset,bbox, plotarea, (1,0),1,(0,140))
        self.sweep(MODES.top, offset,bbox, plotarea, (0,1),2,(0,210))
        self.sweep(MODES.right, offset,bbox, plotarea, (0,1),2,(0,210))
        return


sourcefile = open(sys.argv[1])
plotfile = open(sys.argv[2],'wb')

#image = Image.new("RGB",(1000,1000),"#FFFFFF")
#draw = ImageDraw.Draw(image)

v = Img2Plot(sourcefile,plotfile)
v.draw()

print ("done.")
   
