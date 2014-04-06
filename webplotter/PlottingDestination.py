import time

#PEN
#F000
COLOR = 1
DRAW = 0

    
#left = 0F00, right = 00F0
FWD = 1
REV = 2

#pen position
#000F
UP =  1
DWN = 2
NIL = 0

#pen color
#000F
RED = 0
GREEN = 1
BLUE = 2 
BLACK = 3


class Destination:

    def __init__(self,steppera,stepperb,solenoid,delay):
        self.steppera = steppera
        self.stepperb = stepperb
        self.solenoid = solenoid
        self.delay = delay
        

    def write(self,b):
        sa = (b >> 4) & 3
        sb = (b >> 2) & 3
        pen = b & 3
        # print (sa,sb)
        if (pen == UP):
            self.solenoid.disengage()
        if (pen == DWN):
            self.solenoid.engage()
        if (sb==FWD):
            # print "stepperb up"
            self.stepperb.stepup()
        elif (sb==REV):
            # print "stepperb down"
            self.stepperb.stepdown()
        if (sa == FWD):
            # print "steppera up"
            self.steppera.stepup()
        elif (sa == REV):
            # print "steppera down"
            self.steppera.stepdown()
        time.sleep(self.delay)


    
