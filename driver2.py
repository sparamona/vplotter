#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod

from Plotter import Lengths, Point, Plotter
from servo import Servo
from stepper2 import Stepper

class Driver(Plotter):

    def __init__(self,steppera,stepperb,pen,plotfile,delay):
        Plotter.__init__(self,plotfile)
        self.steppera = steppera
        self.stepperb = stepperb
        self.pen = pen
        self.delay = delay


    def run(self):

        while True:
            c = (self.plotfile.read(1))
            if c==b'':
                break
            b = c[0]
        

            # print "read ", b
            sa = (b >> 4) & 3
            sb = (b >> 2) & 3
            pen = b & 3
            # print (sa,sb)
            if (pen == Driver.UP):
                self.pen.up()
            if (pen == Driver.DWN):
                self.pen.down()
            if (sb==Driver.FWD):
                #print("stepperb up")
                self.stepperb.stepup()
            elif (sb==Driver.REV):
                #print("stepperb down")
                self.stepperb.stepdown()
            if (sa == Driver.FWD):
                #print("steppera up")
                self.steppera.stepup()
            elif (sa == Driver.REV):
                #print("steppera down")
                self.steppera.stepdown()
            time.sleep(self.delay)
    

def BuildDriver(plotfile):
    steppera = Stepper(True)
    stepperb = Stepper(False)
    pen = Servo()
    v = Driver(steppera,stepperb,pen,plotfile,0.02)
    return v


def main():
    plotfile = open(sys.argv[1],'rb')
    d = BuildDriver(plotfile)
    d.run()

   
