#!/usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Lengths,Point,Plotter
from PIL import Image, ImageEnhance

def inbox(p,box):
    return (p.x>=box[0]) and (p.x<=box[2]) and (p.y>=box[1]) and (p.y<=box[3])


class MODES:
    EW=1
    NS=2
    NWSE=3
    NESW=4

    def step_EW(p,step):
        return Point(p.x+step,p.y)
    def step_NS(p,step):
        return Point(p.x,p.y+step)
    def step_NWSE(p,step):
        return Point(p.x+step/2,p.y+step/2)
    def step_NESW(p,step):
        return Point(p.x-step/2,p.y+step/2)

    def start_EW(i,imageArea):
        return Point(imageArea[0],i)
    def start_NS(i,imageArea):
        return Point(i,imageArea[1])
    def start_NWSE(i,imageArea):
        return Point(i,imageArea[0])
    def start_NESW(i,imageArea):
        return Point(i,imageArea[0])


    def range_EW(imageArea,width):
        return range(imageArea[1],imageArea[3],width)
    def range_NS(imageArea,width):
        return range(imageArea[0],imageArea[2],width)
    def range_NWSE(imageArea,width):
        height = (imageArea[3]-imageArea[1])
        return range(imageArea[0]-height,imageArea[2],width)
    def range_NESW(imageArea,width):
        height = (imageArea[3]-imageArea[1])
        return range(imageArea[0],imageArea[2]+height,width)

    _funcs = { EW:(step_EW,  start_EW,  range_EW,   (1.0,0.0)),
               NS:(step_NS,  start_NS,  range_NS,   (0.0,1.0)),
               NWSE:(step_NWSE,start_NWSE,range_NWSE, (1.0,1.0)),
               NESW:(step_NESW,start_NESW,range_NESW, (-1.0,1.0)) }

    @staticmethod
    def step(mode,p,step):
        return MODES._funcs[mode][0](p,step)

    @staticmethod
    def start(mode,i,imageArea):
        return MODES._funcs[mode][1](i,imageArea)

    @staticmethod
    def range(mode,imageArea,width):
        return MODES._funcs[mode][2](imageArea,width)

    @staticmethod
    def stepDelta(mode):
        return MODES._funcs[mode][3]

class Img2Plot(Plotter):

    def __init__(self,image,plotfile,plotarea):
        Plotter.__init__(self,plotfile)

        # set up
        self.plotarea = plotarea
        self.spacing = 5
        self.image = image
        self.scaleImage()
      
        #shadelevels = self.detectShades(1.0)
        #print ("auto leveled for %s" % (shadelevels))
        #shadelevels = [52,88,150,200]
        #shadelevels = [88,118,150,200]

        startingpoint = [700,700]


    def scaleImage(self):
        bbox = self.image.getbbox()
        dims = (bbox[2],bbox[3])
        plotareaDims=(self.plotarea[2]-self.plotarea[0],self.plotarea[3]-self.plotarea[1])
        if (dims[0]>plotareaDims[0]) or (dims[1]>plotareaDims[1]):
            scaleDims = (float(plotareaDims[0])/float(dims[0]),float(plotareaDims[1])/float(dims[1]))
            # scale by the smallest
            scale = min(scaleDims)
            self.image = image.resize((int(scale*dims[0]),int(scale*dims[1])))
            print("scaling to %s" % scale)
        else:
            self.image = image
        self.image = self.image.convert("L")
        #self.image = ImageEnhance.Contrast(self.image).enhance(contrast)
        #self.image = ImageEnhance.Brightness(self.image).enhance(brightness)
         
        self.imageArea = (self.plotarea[0],self.plotarea[1],
                          min(self.plotarea[2],self.image.getbbox()[2]+self.plotarea[0]),
                          min(self.plotarea[3],self.image.getbbox()[3]+self.plotarea[1]))
        print(self.imageArea)
        print(self.image.getbbox())

        
    def draw(self):
        #allmodes = [MODES.NWSE,MODES.NESW,MODES.EW,MODES.NS]
        allmodes = [MODES.EW,MODES.NS,MODES.NWSE, MODES.NESW]
        #allmodes = [MODES.NWSE,MODES.NS, MODES.NS]
        #allmodes = [MODES.EW]
        #allmodes = [MODES.EW, MODES.NWSE]
        for m in allmodes:
            self.sweep(m)
        return

    def sweep(self,mode):
        r = MODES.range(mode,self.imageArea,self.spacing)
        fwd = True
        for i in r:
            commands = self.sweep1(mode,i)
            fwd = self.write(commands,fwd)
        print("done sweeping")
        return


    def write(self,commands,fwd):
        if (len(commands)==0):
            return fwd
        if (not(fwd)):
            commands.reverse()
        for c in commands:
            if (fwd):
                self.drawLineTo(c[0],False)
                self.drawLineTo(c[1],True)
            else:
                self.drawLineTo(c[1],False)
                self.drawLineTo(c[0],True)
        return not(fwd)
        

    def sweep1(self,mode,i):

        def inbox(p):
            return ((p.x>=self.imageArea[0]) and (p.x<self.imageArea[2])) and ((p.y>=self.imageArea[1]) and (p.y<self.imageArea[3]))
        def offpage(p):
            return ((p.x>self.imageArea[2]) or (p.y>self.imageArea[3]))

        points = []
        p = MODES.start(mode,i,self.imageArea)
        delta = (MODES.stepDelta(mode)[0]*self.stepLength/2.0,
                 MODES.stepDelta(mode)[1]*self.stepLength/2.0)
        offset = Point(self.imageArea[0],self.imageArea[1])
        vrange = self.shades[mode]
        state = 0
        #print p
        inline = False
        startingOffpage = offpage(p)
        _from = p
        while startingOffpage or not(offpage(p)):
            if not(offpage(p)):
                startingOffpage=False
            #print p
            _inbox = inbox(p)
            if _inbox:
                state=1
            elif (state==1) and not(_inbox):
                break
            if _inbox:
                pix = self.image.getpixel((p.x-offset.x,p.y-offset.y))
                pencommand = 2 if (pix>vrange[0] and pix<=vrange[1]) else 1
                if (pencommand==2 and inline==False):
                    # now check to see if the last line was within 2 steps max(X,Y)
                    _from=p
                    if (len(points)>0):
                        lastpoint = points[-1]
                        if max(p.x-lastpoint[1].x,p.y-lastpoint[1].y)<2.0*self.stepLength:
                            #reset _from
                            #print "resetting"
                            points.pop()
                            _from=lastpoint[0]
                    inline=True
                if (pencommand==1 and inline==True):
                    points.append((_from,p))
                    inline=False
            p = Point(p.x+delta[0],p.y+delta[1])

        #close a line
        if (inline==True):
            points.append((_from,p))
        #print len(points)
        #print "ended @ ",p
        return points
            

#
# MAIN
#

sourcefile = sys.argv[1]
plotfile = open(sys.argv[2],'w')
shadelevels = [float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])]


image = Image.open(sourcefile)
margins = [ 250, 250, 250, 300] # left, top, right down
totalarea = (1200, 1700)
plotarea = (margins[0],margins[1],totalarea[0]-margins[2],totalarea[1]-margins[3])


v = Img2Plot(image,plotfile,plotarea, shadelevels)
#shadelevels = v.detectShades(float(shadescale))

v.draw()

print ("done.")
   
