import sys,collections
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod


class Lengths(collections.namedtuple('lengths',['a','b'])):
    '''Lengths'''

class Point(collections.namedtuple('point',['x','y'])):
    '''Point'''



class Plotter:

    #COMMAND
    #F000
    COLOR = 1  # Change color command
    DRAW = 0   # Draw (or move)

    
    #Motor commands for A and B motors
    #left = 0F00, right = 00F0
    FWD = 1
    REV = 2

    #pen position when command = DRAW
    #000F
    UP =  1
    DWN = 2
    NIL = 0

    #pen color in the final 4 bits when command = COLOR
    #000F
    CYAN = 0
    MAGENTA = 1
    YELLOW = 2 
    BLACK = 3


    PIXELS_PER_INCH = 25.40
    
    def __init__(self, plotfile):
        
        #self.W = 942.975                                # 37.125"  -- distance between the motor points, 25.40 pixels per inch
        self.W = 48*Plotter.PIXELS_PER_INCH
        
        self.stepLength = .00314*Plotter.PIXELS_PER_INCH         # MICROSTEPS => 6.28" for 2000 steps ==> .00314" per step
                                                         # distance the belt moves per step      
        #self.startLengths = Lengths(508.0,508.0)        # Starting point (arbitrary, but should be roughly correct)
        self.startLengths = Lengths(676.0,676.0)        # Starting point (arbitrary, but should be roughly correct)
        #self.currentLengths = Lengths(508.0,508.0)  
        self.currentLengths = self.startLengths
        self.plotfile = plotfile
        #self.pixelsPerStep = .1
        self.pixelsPerStep = self.stepLength # not sure why this is different

    _bytes = bytearray(1)
    def write(self,b):
        # skip if it's just a 1 and not moving 
        if (b>2):
            self._bytes[0] = b
            self.plotfile.write(self._bytes)

    def changeColor(self, color):
        print("calling change color %d" % color)
        b = (1 << 6) + color
        try:
           self.write(b)
        except (ValueError):
           print("got value error writing: %s " % b)
           raise ValueError


    def drawLineTo(self,p2,pendown):
        pencommand = 2 if pendown else 1

        p1 = self.pointFromLengths(self.currentLengths)
        #print "drawing from " ,p1, " to ", p2

        last = self.currentLengths

        dx = p2.x-p1.x
        dy = p2.y-p1.y

        d = sqrt(pow(dx,2)+pow(dy,2))
        step = self.pixelsPerStep/d

        i = 0.0
        count = 0
        while i<=1.0:
            count=count+1
            precise = self.lengthsFromPoint(Point(p1.x+dx*i,p1.y+dy*i))
            da = precise.a-last.a
            db = precise.b-last.b
            # do I step?
            sa = 0
            sb = 0
            if fabs(da)>self.stepLength:
                sa = 1 if da > 0 else -1
            if fabs(db)>self.stepLength:
                sb = 1 if db > 0 else -1
            # print "steps: ",[sa,sb]
            b = ((2 if sa<0 else sa) << 4) + ((2 if sb<0 else sb)<<2) + pencommand
            # print "writing ", sa,b
            try:
                self.write(b)
            except (ValueError):
                print("got value error writing: %s " % b)
                raise ValueError
            self.currentLengths = Lengths(last.a+sa*self.stepLength,last.b+sb*self.stepLength)
            last = self.currentLengths
            i += step

    def reset(self):
        self.moveTo(self.startLengths)

    def moveTo(self,to):
        # print "moving to ", to
        steplength=self.stepLength
        fromL=self.currentLengths
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
                break
            self.write(b)
        self.currentLengths=Lengths(la,lb)


    def lengthsFromPoint(self,p):
        l = Lengths(sqrt(p.y**2+p.x**2),sqrt(p.y**2+(self.W-p.x)**2))
        #    print "calculated point ", p, " to lengths ",l, " back to point ", self.pointFromLengths(l)
        #    if (p.x!=p2.x || p.y!=p2.y) print "not equivalent (p
        return l


    def pointFromLengths(self,l):
        #print "running for ",self.W," and ",l
        x = (l.a**2-l.b**2+self.W**2)/(2*self.W*l.a)
        try:
            al=acos(x)
            #print "got al = ", degrees(al)
            return Point(l.a*cos(al),l.a*sin(al))
        except (ValueError):
            if (l.a+l.b)<self.W:
                print('offsetting')
                return self.pointFromLengths(Lengths(l.a+(l.a+l.b-self.W),l.b))
            else:
                print("ValueError for %s" & l)
                raise ValueError

        
    def printSteps(self,bts):
        a=0
        b=0
        for s in bts:
            a+=(s>>4&1)
            a-=(s>>4&2)
            b+=(s>>2&1)
            b-=(s>>2&2)
        print("a="+str(a)+"; b="+str(b))
