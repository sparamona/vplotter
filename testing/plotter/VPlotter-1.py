#!/usr/bin/env python
import sys,Image,ImageDraw,collections
from math import sqrt,sin,cos,acos,atan2,degrees,fabs


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
    return (l.a*cos(al),l.a*sin(al))


def cross(draw,p,n):
    c="#000000"
    draw.line((p[0],p[1]-n,p[0],p[1]+n),c)
    draw.line((p[0]-n,p[1],p[0]+n,p[1]),c)


class VPlotter:

    def __init__(self,image,W):
        self.image=image
        self.W=W

    def drawPoint(self,p):
        l = lengthsFromPoint(self.W,p)
        self.drawAtLengths(l)
        
    def drawAtLengths(self,l):
        BLACK="#000000"
        p = pointFromLengths(self.W,l)
        # print "drawing ",l, " at ",p
        draw.point((round(p[0]),round(p[1])),BLACK)
        #cross(draw,p,10)
    

image = Image.new("RGB",(1000,1000),"#D0D0D0")
draw = ImageDraw.Draw(image)

v = VPlotter(draw,1000.0)
for a in range(300,700):
    v.drawPoint(Point(a,500.0))

image.show()
image.save("out.png","PNG")
print ("done.")
   
