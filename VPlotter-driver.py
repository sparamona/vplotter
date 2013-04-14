#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from stepperStub import Stepper


class Lengths(collections.namedtuple('lengths',['a','b'])):
    '''Lengths'''

class Point(collections.namedtuple('point',['x','y'])):
    '''Point'''

class VPlotter:

    FWD = 1
    REV = 2
    UP =  1
    DWN = 2
    NIL = 0

    def __init__(self,steppera,stepperb,plotfile,delay):
        self._p = Point(0.0,0.0)
        self.steppera = steppera
        self.stepperb = stepperb
        self.out = plotfile
        self.pen = VPlotter.DWN
        self.f = plotfile
        self.delay = delay

    def draw(self):

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
                self.steppera.stepup()
            elif (sa == VPlotter.REV):
                # print "steppera down"
                self.steppera.stepdown()
            if (sb==VPlotter.FWD):
                # print "stepperb up"
                self.stepperb.stepup()
            elif (sb==VPlotter.REV):
                # print "stepperb down"
                self.stepperb.stepdown()
            time.sleep(self.delay)

    

steppera = Stepper(18,4,17,23,24)
stepperb = Stepper(18,22,14,15,25)
plotfile = open('out.plot','rb')

v = VPlotter(steppera,stepperb,plotfile,0.01)
v.draw()
#for a in range(300,700):
#    v.drawPoint(Point(a,500.0))
#v.drawLine(Point(0.0,0.0),Point(300.0,500.0),False)
#v.drawLine(Point(300.0,500.0),Point(700.0,500.0),True)
#v.drawLine(Point(700.0,500.0),Point(700.0,400.0),True)
#v.drawLine(Point(700.0,400.0),Point(300.0,400.0),True)
#v.drawLine(Point(300.0,400.0),Point(300.0,500.0),True)

#image.show()
#image.save("out.png","PNG")
print ("done.")
   
