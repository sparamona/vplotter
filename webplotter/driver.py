#!/usr/bin/env python
from stepperStub import Stepper
from Plotter import Lengths, Point, Plotter
from solenoidStub import Solenoid
from PlottingDestination import Destination

class Driver(Plotter):

    def __init__(self,destination):
        Plotter.__init__(self,destination)

    def run(self):
        self.moveTo(self.lengthsFromPoint(Point(100,100)))
        self.drawLineTo(Point(100,200), Driver.DWN)
    

stepperb = Stepper(18,4,17,23,24)
steppera = Stepper(18,22,14,15,25)
solenoid = Solenoid()
delay = 0.004
destination = Destination(steppera,stepperb,solenoid, delay)

v = Driver(destination)
v.run()
print ("done.")
   
