#!/usr/bin/env python
import sys,collections,gc,time,Image
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Lengths,Point,Plotter

def inbox(p,box,offset):
    return (p.x-offset.x>=box[0]) and (p.x-offset.x<=box[2]) and (p.y-offset.y>=box[1]) and (p.y-offset.y<=box[3])


class Img2Plot(Plotter):

    def __init__(self,sourcefile,plotfile):
        Plotter.__init__(self,plotfile)
        self.im = Image.open(sourcefile)


    def draw(self):
        steplength = self.stepLength

        # fix b first
        bbox = self.im.getbbox()
        offset = Point(200,100)
        print bbox

        for i in range(bbox[0]+offset.x,bbox[2]+offset.x+200,5):
            print "on row ",i
            l = self.lengthsFromPoint(Point(i,offset.y))
            self.moveTo(l)
            while True:
                # now add keep adding B steps only, and use penup/pendown
                l=Lengths(l.a,l.b+steplength)
                p = self.pointFromLengths(l)
                #print "at point ",p
                if p.y>bbox[3]+offset.y or p.x<=offset.x:
                    break
                try: 
                    if inbox(p,bbox,offset):
                        pix = self.im.getpixel((p.x-offset.x,p.y-offset.y))
                        pencommand = 2 if (pix[2]<=255/2) else 1
                    else:
                        pencommand=1
                    b = (0 << 4) + (1<<2) + pencommand
                    self.plotfile.write(chr(b))
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
                self.currentLengths=l
    
        for i in range(bbox[0]+offset.x-200,bbox[2]+offset.x,5):
            print "on row ",i
            l = self.lengthsFromPoint(Point(i,offset.y))
            self.moveTo(l)
            while True:
                # now add keep adding A steps only, and use penup/pendown
                l=Lengths(l.a+steplength,l.b)
                p = self.pointFromLengths(l)
                # print "at point ",p
                if p.y>=bbox[3]+offset.y or p.x>=bbox[2]+offset.x: 
                    break
                try: 
                    if inbox(p,bbox,offset):
                        pix = self.im.getpixel((p.x-offset.x,p.y-offset.y))
                        pencommand = 2 if (pix[1]<=255/2) else 1
                    else:
                        pencommand=1
                    b = (1 << 4) + (0<<2) + pencommand
                    self.plotfile.write(chr(b))
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
                self.currentLengths=l


        for i in range(bbox[1]+offset.y,bbox[3]+offset.y,5):
            print "on row ",i
            l = self.lengthsFromPoint(Point(offset.x,i))
            self.moveTo(l)
            while True:
                # now add keep adding A and B steps, and use penup/pendown
                l=Lengths(l.a+steplength,l.b+steplength if i+offset.x<self.W else l.b-steplength)
                p = self.pointFromLengths(l)
                # print "at point ",p
                if p.y>=bbox[3]+offset.y or p.x>=bbox[2]+offset.x: 
                    break
                try: 
                    if inbox(p,bbox,offset):
                        pix = self.im.getpixel((p.x-offset.x,p.y-offset.y))
                        pencommand = 2 if (pix[2]<=255/2) else 1
                    else:
                        pencommand=1
                    b = (1 << 4) + ((1 if i+offset.x<self.W else 2) <<2) + pencommand
                    self.plotfile.write(chr(b))
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
                self.currentLengths=l



sourcefile = open(sys.argv[1])
plotfile = open(sys.argv[2],'wb')

#image = Image.new("RGB",(1000,1000),"#D0D0D0")
#draw = ImageDraw.Draw(image)

v = Img2Plot(sourcefile,plotfile)
v.draw()

print ("done.")
   
