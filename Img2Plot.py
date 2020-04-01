#!/usr/bin/env python
import sys,collections,gc,time
from PIL import Image
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Lengths,Point,Plotter

def inbox(p,box):
    return (p.x>=box[0]) and (p.x<=box[2]) and (p.y>=box[1]) and (p.y<=box[3])


class MODES:
    left=0
    right=1
    top=2
    bottom=3

class Img2Plot(Plotter):

    def __init__(self,sourcefile,plotfile):
        Plotter.__init__(self,plotfile)
        print("opening sourcefile %s" % sourcefile)
        self.im = Image.open(sourcefile)
        self.im = self.im.convert("L")

   
    def sweep(self, mode, offset, bbox, plotarea, direction, rgb, vrange, color,density,range_offset):
       colorcommand = (Plotter.COLOR<<6) + color
       self.plotfile.write(chr(colorcommand))        
       if (mode==MODES.top) or (mode==MODES.bottom):
           r=range(bbox[0],bbox[2],density)
       elif (mode==MODES.left) or (mode==MODES.right):
           r=range(bbox[1]+range_offset,bbox[3],density)

       for i in r:
            sys.stdout.write('.')
            sys.stdout.flush()
            if mode==MODES.top:
                movetop = Point(i,offset.y+1)
            elif mode==MODES.bottom:
                movetop = Point(i,bbox[3]-1)
            elif mode==MODES.left:
                movetop = Point(offset.x+1,i)
            elif mode==MODES.right:
                movetop = Point(bbox[2]-1,i)
            self.moveTo(self.lengthsFromPoint(movetop))
            l = self.currentLengths
            state = 0

            lastWrittenLength=self.currentLengths
            writeLength = 0
            commands = []
            stepa = direction[0] if direction[0]>=0 else 2
            stepb = direction[1] if direction[1]>=0 else 2

            while True:
                # now add keep adding steps, and use penup/pendown
                l=Lengths(l.a+direction[0]*self.stepLength,l.b+direction[1]*self.stepLength)
                p = self.pointFromLengths(l)
                #print "at point ",p
                if state==2 or (inbox(p,plotarea)==False):
                    # print "break", len(commands), plotarea, p, l
                    break
                try: 
                    if inbox(p,bbox):
                        pix = self.im.getpixel((p.x-offset.x,p.y-offset.y))
                        #print pix
                        #pencommand = 2 if (pix[rgb]>vrange[0] and pix[rgb]<=vrange[1]) else 1
                        pencommand = 2 if (pix>vrange[0] and pix<=vrange[1]) else 1
                        state = 1
                    else:
                        pencommand=1
                        if state==1:
                            state=2
                    b = (stepa<<4) + (stepb<<2) +  pencommand
                    # self.plotfile.write(chr(b))
                    commands.append(b)
                    if (pencommand==2):
                        writeLength=len(commands)
                        lastWrittenLength = l
                    self.currentLengths=l
                except (IndexError):
                    print("got index error on pixel: %s " % p)
                    raise IndexError
            # now write out the buffer, and set the currentLengths
            self.currentLengths=lastWrittenLength
            for c in commands[0:writeLength]:
                self.plotfile.write(chr(c))

        

    def draw(self):

        # fix b first
        margin = 200
        offset = Point(margin,margin)
        plotarea = (margin,margin,int(self.W-margin),int(self.W-margin))

        bbox = (max(plotarea[0],offset.x),
                max(plotarea[1],offset.y),
                min(plotarea[2],self.im.getbbox()[2]+offset.x),
                min(plotarea[3],self.im.getbbox()[3]+offset.y))
        print(bbox)

#        self.sweep(MODES.top, offset,bbox, plotarea, (1,1),0,(127,255), Plotter.RED)
#        self.sweep(MODES.top, offset,bbox, plotarea, (1,0),1, (127,255), Plotter.GREEN)
#        self.sweep(MODES.left, offset,bbox, plotarea, (1,0),1,(127,255), Plotter.GREEN)
#        self.sweep(MODES.top, offset,bbox, plotarea, (0,1),2,(127,255), Plotter.BLUE)
#        self.sweep(MODES.right, offset,bbox, plotarea, (0,1),2,(127,255), Plotter.BLUE)

        self.sweep(MODES.top, offset,bbox, plotarea, (1,1),0,(0,80), Plotter.BLACK,4,4)
        self.sweep(MODES.top, offset,bbox, plotarea, (1,0),0, (0,140), Plotter.BLACK,4,4)
        self.sweep(MODES.left, offset,bbox, plotarea, (1,0),0,(0,140), Plotter.BLACK,9,4)
        self.sweep(MODES.left, offset,bbox, plotarea, (1,-1),0,(0,170), Plotter.BLACK,4,4)
        self.sweep(MODES.top, offset,bbox, plotarea, (1,-1),0,(0,170), Plotter.BLACK,18,4)
        self.sweep(MODES.top, offset,bbox, plotarea, (0,1),0,(0,200), Plotter.BLACK,4,4)
        self.sweep(MODES.right, offset,bbox, plotarea, (0,1),0,(0,200), Plotter.BLACK,9,8) # 4 for ANS, 8 for VB
        return


#sourcefile = open(sys.argv[1])
sourcefile = sys.argv[1]
plotfile = open(sys.argv[2],'w')

#image = Image.new("RGB",(1000,1000),"#FFFFFF")
#draw = ImageDraw.Draw(image)

v = Img2Plot(sourcefile,plotfile)
v.draw()

print ("done.")
   
