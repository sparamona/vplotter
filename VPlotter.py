#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from stepper import Stepper

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


#def cross(draw,p,n):
#    c="#000000"
#    draw.line((p[0],p[1]-n,p[0],p[1]+n),c)
#    draw.line((p[0]-n,p[1],p[0]+n,p[1]),c)
#    print "drawing cross @ ", p


class VPlotter:

    def __init__(self,steppera,stepperb,W):
        self.W=W
        self._p = Point(0.0,0.0)
        self.steppera = steppera
        self.stepperb = stepperb

    def moveTo(self,l):
        print "pen up"
        print "moving to lengths ",l


    def drawLine(self,p1,p2):
        # garbage collect beforehand
        print "gc.collect() start"
        #gc.collect()
        print "gc.collect() done"
        v = .1 # pixels per step
        steplength = .1

        dx = p2.x-p1.x
        dy = p2.y-p1.y

        d = sqrt(pow(dx,2)+pow(dy,2))

        print "distance: ", d

        l1 = lengthsFromPoint(self.W,p1)
        self.moveTo(l1)
        # find left and right deltas

        step = v/d
        last = l1
        i = 0.0
        while i<=1.0:
            precise = lengthsFromPoint(self.W,Point(p1.x+dx*i,p1.y+dy*i))
            da = precise.a-last.a
            db = precise.b-last.b
            # do I step?
            sa = 0
            sb = 0
            if fabs(da)>steplength:
                sa = 1 if da > 0 else -1
            if fabs(db)>steplength:
                sb = 1 if db > 0 else -1
            # print "steps: ",[sa,sb]
            steppera.step(sa)
            stepperb.step(sb)
            current = Lengths(last.a+sa*steplength,last.b+sb*steplength)
            last = current
            #self.drawAtLengths(current)
            time.sleep(0.005)
            i += step
        

    def drawPoint(self,p):
        l = lengthsFromPoint(self.W,p)
        self.drawAtLengths(l)
        
    def drawAtLengths(self,l):
        #BLACK="#000000"
        p = pointFromLengths(self.W,l)
        #print "drawing ",l, " at ",p
        #draw.point((round(p[0]),round(p[1])),BLACK)
        #cross(draw,p,10)
    

steppera = Stepper(18,4,17,23,24)
stepperb = Stepper(18,22,14,15,25)

#image = Image.new("RGB",(1000,1000),"#D0D0D0")
#draw = ImageDraw.Draw(image)

v = VPlotter(steppera,stepperb,1000.0)
#for a in range(300,700):
#    v.drawPoint(Point(a,500.0))
v.drawLine(Point(300.0,500.0),Point(700.0,500.0))
v.drawLine(Point(700.0,500.0),Point(700.0,400.0))
v.drawLine(Point(700.0,400.0),Point(300.0,400.0))
v.drawLine(Point(300.0,400.0),Point(300.0,500.0))

#image.show()
#image.save("out.png","PNG")
print ("done.")
   
