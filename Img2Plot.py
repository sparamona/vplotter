#!/usr/bin/env python
import sys,collections,gc,time,Image
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod

class Lengths(collections.namedtuple('lengths',['a','b'])):
    '''Lengths'''

class Point(collections.namedtuple('point',['x','y'])):
    '''Point'''

def lengthsFromPoint(W,p):
    l = Lengths(sqrt(p.y**2+p.x**2),sqrt(p.y**2+(W-p.x)**2))
    #    print "calculated point ", p, " to lengths ",l, " back to point ", pointFromLengths(W,l)
    #    if (p.x!=p2.x || p.y!=p2.y) print "not equivalent (p
    return l


def pointFromLengths(W,l):
    al=acos((l.a**2-l.b**2+W**2)/(2*W*l.a))
    # print "got al = ", degrees(al)
    return Point(l.a*cos(al),l.a*sin(al))


#def cross(draw,p,n):
#    c="#000000"
#    draw.line((p[0],p[1]-n,p[0],p[1]+n),c)
#    draw.line((p[0]-n,p[1],p[0]+n,p[1]),c)
#    print "drawing cross @ ", p


def inbox(p,box,offset):
    return (p.x-offset.x>=box[0]) and (p.x-offset.x<=box[2]) and (p.y-offset.y>=box[1]) and (p.y-offset.y<=box[3])


class VPlotter:

    def __init__(self,W,sourcefile,plotfile):
        self.W=W
        self._p = Point(0.0,0.0)
        self.out = plotfile
        self.im = Image.open(sourcefile)
        self._l = Lengths(0.15,W)

    def moveTo(self,to):
        print "moving to ", to
        steplength=.15
        fromL=self._l
        toL=to
        direction = Lengths(1 if fromL.a<=toL.a else -1,1 if fromL.b<=toL.b else -1)
        #print direction
        la = fromL.a
        lb = fromL.b
        while True:
            #print "l= ",(la,lb)
            stepa=0
            stepb=0
            if (direction.a>0):
                if la<toL.a:
                    stepa=1
                    la=la+steplength
            else:
                if la>toL.a:
                    stepa=2
                    la=la-steplength
            if (direction.b>0):
                if lb<toL.b:
                    stepb=1
                    lb=lb+steplength
            else:
                if lb>toL.b:
                    stepb=2
                    lb=lb-steplength
            b = (stepa << 4) + (stepb<<2) + 1
            if stepa==0 and stepb==0:
                break;
            self.out.write(chr(b))
        self._l=Lengths(la,lb)

    def draw(self):
        steplength = .15

        # fix b first
        bbox = self.im.getbbox()
        offset = Point(200,100)
        print bbox

        for i in range(bbox[0]+offset.x,bbox[2]+offset.x+200,5):
            print "on row ",i
            l = lengthsFromPoint(self.W,Point(i,offset.y))
            self.moveTo(l)
            while True:
                # now add keep adding B steps only, and use penup/pendown
                l=Lengths(l.a,l.b+steplength)
                p = pointFromLengths(self.W,l)
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
                    self.out.write(chr(b))
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
                self._l=l

    
        for i in range(bbox[0]+offset.x-200,bbox[2]+offset.x,5):
            print "on row ",i
            l = lengthsFromPoint(self.W,Point(i,offset.y))
            self.moveTo(l)
            while True:
                # now add keep adding A steps only, and use penup/pendown
                l=Lengths(l.a+steplength,l.b)
                p = pointFromLengths(self.W,l)
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
                    self.out.write(chr(b))
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
                self._l=l


        for i in range(bbox[1]+offset.y,bbox[3]+offset.y,5):
            print "on row ",i
            l = lengthsFromPoint(self.W,Point(offset.x,i))
            self.moveTo(l)
            while True:
                # now add keep adding A and B steps, and use penup/pendown
                l=Lengths(l.a+steplength,l.b+steplength if i+offset.x<self.W else l.b-steplength)
                p = pointFromLengths(self.W,l)
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
                    self.out.write(chr(b))
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
                self._l=l



sourcefile = open('shiney.jpg')
plotfile = open('out.plot','wb')

#image = Image.new("RGB",(1000,1000),"#D0D0D0")
#draw = ImageDraw.Draw(image)

v = VPlotter(1000.0,sourcefile,plotfile)
v.draw()

print ("done.")
   
