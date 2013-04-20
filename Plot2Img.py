#!/Usr/bin/env python
import sys,collections,gc,time
from math import sqrt,sin,cos,acos,atan2,degrees,fabs,pow,modf,fmod
import Image,ImageDraw
from Plotter import Lengths, Point, Plotter

class Plot2Img(Plotter):

    def __init__(self,image,plotfile):
        Plotter.__init__(self,plotfile)
        self.image = image


    def draw(self):

        _a = self.currentLengths.a
        _b = self.currentLengths.b

        while True:
            c = (self.plotfile.read(1))
            if c==b'':
                break
            b = bytearray(c)[0]
        

            # print "read ", b
            sa = (b >> 4) & 3
            sb = (b >> 2) & 3
            pen = b & 3
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
                self.image.point(p,"#000000")

    

width = 1000
height= 1000
image = Image.new("RGB",(width,height),"#D0D0D0")
draw = ImageDraw.Draw(image)
plotfile = open(sys.argv[1],'rb')
v = Plot2Img(draw,plotfile)
v.draw()

image.show()
#image.save("out.png","PNG")
print ("done.")
   
