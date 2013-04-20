import sys,collections
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod


class Lengths(collections.namedtuple('lengths',['a','b'])):
    '''Lengths'''

class Point(collections.namedtuple('point',['x','y'])):
    '''Point'''



class Plotter:

    FWD = 1
    REV = 2
    UP =  1
    DWN = 2
    NIL = 0



    def __init__(self, plotfile):
        self.W = 942.975 # 37.125"
        self.stepLength = .15
        self.startLengths = Lengths(508.0,508.0)
        self.currentLengths = Lengths(508.0,508.0)
        self.plotfile = plotfile
        self.pixelsPerStep = .1


    def drawLineTo(self,p2,pendown):
        pencommand = 2 if pendown else 1

        p1 = self.pointFromLengths(self.currentLengths)
        print "drawing from " ,p1, " to ", p2

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
                self.plotfile.write(chr(b))
            except (ValueError):
                print "got value error writing ", b
                raise ValueError
            self.currentLengths = Lengths(last.a+sa*self.stepLength,last.b+sb*self.stepLength)
            last = self.currentLengths
            i += step

    def reset(self):
        self.moveTo(self.startLengths)

    def moveTo(self,to):
        print "moving to ", to
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
                break;
            self.plotfile.write(chr(b))
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
                print 'offsetting'
                return self.pointFromLengths(Lengths(l.a+(l.a+l.b-self.W),l.b))
            else:
                print "ValueError for ",l
                raise ValueError

        

