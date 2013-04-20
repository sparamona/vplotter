#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from stepper import Stepper
from Plotter import Lengths, Point, Plotter

class Driver(Plotter):


    def __init__(self,steppera,stepperb,plotfile,delay):
        Plotter.__init__(self,plotfile)
        self.steppera = steppera
        self.stepperb = stepperb
        self.delay = delay

    def run(self):

        while True:
            c = (self.plotfile.read(1))
            if c==b'':
                break
            b = bytearray(c)[0]
        

            # print "read ", b
            sa = (b >> 4) & 3
            sb = (b >> 2) & 3
            pen = b & 3
            # print (sa,sb)
            if (sb==Driver.FWD):
                # print "stepperb up"
                self.stepperb.stepup()
            elif (sb==Driver.REV):
                # print "stepperb down"
                self.stepperb.stepdown()
            if (sa == Driver.FWD):
                # print "steppera up"
                self.steppera.stepup()
            elif (sa == Driver.REV):
                # print "steppera down"
                self.steppera.stepdown()
            time.sleep(self.delay)

    

stepperb = Stepper(18,4,17,23,24)
steppera = Stepper(18,22,14,15,25)
plotfile = open(sys.argv[1],'rb')

v = Driver(steppera,stepperb,plotfile,0.005)
v.run()
print ("done.")
   
