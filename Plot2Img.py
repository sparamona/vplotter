#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
import Image,ImageDraw


class Lengths(collections.namedtuple('lengths',['a','b'])):
    '''Lengths'''

class Point(collections.namedtuple('point',['x','y'])):
    '''Point'''

def pointFromLengths(W,l):
    #print "running for ",W," and ",l
    x = (l.a**2-l.b**2+W**2)/(2*W*l.a)
    try:
        al=acos(x)
        #print "got al = ", degrees(al)
        return (l.a*cos(al),l.a*sin(al))
    except (ValueError):
        if (l.a+l.b)<W:
            print 'offsetting'
            return pointFromLengths(W,Lengths(l.a+(l.a+l.b-W),l.b))
        else:
            print "ValueError for ",l
        raise ValueError


class VPlotter:

    FWD = 1
    REV = 2
    UP =  1
    DWN = 2
    NIL = 0

    def __init__(self,image,plotfile,W,steplength):
        self.startlengths = Lengths(600.0,600.0)
        self.out = plotfile
        self.pen = VPlotter.DWN
        self.f = plotfile
        self.image=image
        self.W=W
        self.steplength=steplength

    def draw(self):

        _a = self.startlengths.a
        _b = self.startlengths.b

        while True:
            c = (self.f.read(1))
            if c==b'':
                break
            b = bytearray(c)[0]
        

            # print "read ", b
            sa = (b >> 4) & 3
            sb = (b >> 2) & 3
            pen = b & 3
            if (sa == VPlotter.FWD):
                # print "steppera up"
                _a=_a+self.steplength
            elif (sa == VPlotter.REV):
                # print "steppera down"
                _a=_a-self.steplength
            if (sb==VPlotter.FWD):
                # print "stepperb up"
                _b=_b+self.steplength
            elif (sb==VPlotter.REV):
                # print "stepperb down"
                _b=_b-self.steplength
            p = pointFromLengths(self.W,Lengths(_a,_b))
            if pen==VPlotter.DWN:
                self.image.point(p,"#000000")

    

width = 1000
height= 1000
image = Image.new("RGB",(width,height),"#D0D0D0")
draw = ImageDraw.Draw(image)
plotfile = open(sys.argv[1],'rb')
v = VPlotter(draw,plotfile,1000.0,.15)
v.draw()

image.show()
#image.save("out.png","PNG")
print ("done.")
   
