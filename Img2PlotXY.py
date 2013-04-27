#!/usr/bin/env python
import sys,collections,gc,time,Image
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
        self.im = Image.open(sourcefile)
        self.im = self.im.convert("L")
        

    def sweep(self, mode, offset, bbox, plotarea, direction, rgb, vrange, color):
       colorcommand = (Plotter.COLOR<<6) + color
       #self.plotfile.write(chr(colorcommand))        

       if (mode==MODES.top) or (mode==MODES.bottom):
           r=range(bbox[0],bbox[2],6)
       elif (mode==MODES.right):
           r=range(bbox[1]+5,bbox[3],6)
       elif (mode==MODES.left):
           r=range(bbox[1]+7,bbox[3],6)

       for i in r:
            sys.stdout.write('.')
            sys.stdout.flush()

            if mode==MODES.top:
                movetop = Point(i,offset.y+1)
            elif mode==MODES.left:
                movetop = Point(offset.x+1,i)
            elif mode==MODES.right:
                movetop = Point(bbox[2]-1,i)
            self.moveTo(self.lengthsFromPoint(movetop))
            l = self.currentLengths
            precise = movetop

            state = 0

            lastWrittenLength=self.currentLengths
            writeLength = 0
            commands = []


            while True:
                # now add keep adding steps, and use penup/pendown
                #l=Lengths(l.a+direction[0]*self.stepLength,l.b+direction[1]*self.stepLength)
                #p = self.pointFromLengths(l)
                precise = Point(precise.x+direction[0]*self.stepLength/2,precise.y+direction[1]*self.stepLength/2)
                # do I step?
                precisel = self.lengthsFromPoint(precise)
                da = precisel.a-l.a
                db = precisel.b-l.b

                stepa = 0
                stepb = 0

                if fabs(da)>self.stepLength:
                    stepa = 1 if da >= 0 else -1
                if fabs(db)>self.stepLength:
                    stepb = 1 if db >= 0 else -1
                # b = ((2 if stepa<0 else stepa) << 4) + ((2 if stepb<0 else stepb)<<2 + pencommand
                # p = self.pointFromLengths(l)
                # print "at point ",p
                l = Lengths(l.a+stepa*self.stepLength,l.b+stepb*self.stepLength)

                if state==2 or (inbox(precise,plotarea)==False):
                    break
                try: 
                    if inbox(precise,bbox):
                        pix = self.im.getpixel((precise.x-offset.x,precise.y-offset.y))
                        #print pix
                        #pencommand = 2 if (pix[rgb]>vrange[0] and pix[rgb]<=vrange[1]) else 1
                        pencommand = 2 if (pix>vrange[0] and pix<=vrange[1]) else 1
                        state = 1
                    else:
                        pencommand=1
                        if state==1:
                            state=2
                    b = ((2 if stepa<0 else stepa) <<4) + ((2 if stepb<0 else stepb) <<2) +  pencommand
                    # self.plotfile.write(chr(b))
                    commands.append(b)
                    if (pencommand==2):
                        writeLength=len(commands)
                        lastWrittenLength = l
                    self.currentLengths=l
                except (IndexError):
                    print "got index error on pixel ",p
                    raise IndexError
            # now write out the buffer, and set the currentLengths
            self.currentLengths=lastWrittenLength
            for c in commands[0:writeLength]:
                self.plotfile.write(chr(c))

        

    def draw(self):

        # fix b first
        margin = 270  # That leaves a page of roughly 500x500
        offset = Point(margin,margin)
        plotarea = (margin,margin,int(self.W-margin),int(self.W-margin))

        bbox = (max(plotarea[0],offset.x),
                max(plotarea[1],offset.y),
                min(plotarea[2],self.im.getbbox()[2]+offset.x),
                min(plotarea[3],self.im.getbbox()[3]+offset.y))
        print bbox


        #diagonal top left -> bottom right
        self.sweep(MODES.left, offset,bbox, plotarea, (1,1),0, (0,200), Plotter.BLACK)
        self.sweep(MODES.top, offset,bbox, plotarea,  (1,1),0, (0,200), Plotter.BLACK)

        #diagonal top right -> bottom left
        self.sweep(MODES.right, offset,bbox, plotarea, (-1,1),0,(0,170), Plotter.BLACK)
        self.sweep(MODES.top, offset,bbox, plotarea,   (-1,1),0,(0,170), Plotter.BLACK)


        # horizontal
        self.sweep(MODES.left, offset,bbox, plotarea, (1,0),0,(0,140), Plotter.BLACK)


        # vertical
        self.sweep(MODES.top, offset,bbox, plotarea, (0,1),0,(0,80), Plotter.BLACK)

        return


sourcefile = open(sys.argv[1])
plotfile = open(sys.argv[2],'wb')

#image = Image.new("RGB",(1000,1000),"#FFFFFF")
#draw = ImageDraw.Draw(image)

v = Img2Plot(sourcefile,plotfile)
v.draw()

print ("done.")
   
