#!/Usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
from Plotter import Lengths, Point, Plotter
from PIL import Image, ImageDraw


class Plot2Img(Plotter):

    def __init__(self,image,plotfile):
        Plotter.__init__(self,plotfile)
        self.image = image
        self.color = "#000000"


    def draw(self):

        _a = self.currentLengths.a
        _b = self.currentLengths.b

        while True:
            c = (self.plotfile.read(1))
            if c==b'':
                break
            b = bytearray(c)[0]

            # print "read ", b
            command = (b >> 6) & 3
            sa = (b >> 4) & 3
            sb = (b >> 2) & 3
            pen = b & 3
            if (command == Plot2Img.COLOR):
                if (pen==Plot2Img.CYAN):
                    self.color = "#00FFFF"
                if (pen==Plot2Img.MAGENTA):
                    self.color = "#FF00FF"
                if (pen==Plot2Img.YELLOW):
                    self.color = "#FFFF00"
                if (pen==Plot2Img.BLACK):
                    self.color = "#000000"
                continue
            if (sa == Plot2Img.FWD):
                # print "steppera up"
                _a=_a+self.stepLength
            elif (sa == Plot2Img.REV):
                # print "steppera down"
                _a=_a-self.stepLength
            if (sb==Plot2Img.FWD):
                # print "stepperb up"
                _b=_b+self.stepLength
            elif (sb==Plot2Img.REV):
                # print "stepperb down"
                _b=_b-self.stepLength
            p = self.pointFromLengths(Lengths(_a,_b))
            if pen==Plot2Img.DWN:
                self.image.point(p,self.color)

    

width = 1200
height= 1700
image = Image.new("RGB",(width,height),"#FFFFFF")
draw = ImageDraw.Draw(image)
plotfile = open(sys.argv[1],'rb')
v = Plot2Img(draw,plotfile)
v.draw()

#image.show()
image.save(sys.argv[2],"PNG")
print ("done.")
   
