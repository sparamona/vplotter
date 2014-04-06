import web, threading, json
from stepperStub import Stepper
from Plotter import Lengths, Point, Plotter
from solenoidStub import Solenoid
from PlottingDestination import Destination


stepperb = Stepper(18,4,17,23,24)
steppera = Stepper(18,22,14,15,25)
solenoid = Solenoid()
delay = 0.004
#delay = 0
destination = Destination(steppera,stepperb,solenoid, delay)
plotter = Plotter(destination)



class Safety:
    def __init__(self, action):
        self.action = action
        self.t = None

    def start(self):
        print "starting safety"
        self.t = threading.Timer(5.0, self.action)
        self.t.start()

    def stop(self):
        if (self.t != None):
            print "canceling safety"
            self.t.cancel()
        
def penup():
    solenoid.disengage()

safety = Safety(penup)

        
urls = (
    '/move/(\d+)/(\d+)', 'Move',
    '/draw/(\d+)/(\d+)', 'Draw',
    '/reset', 'Reset'
)
app = web.application(urls, globals())

class Move:        
    def GET(self, x, y):
        print 'move to ' + x + ',' + y
        plotter.moveTo(plotter.lengthsFromPoint(Point(int(x),int(y))))
        return json.dumps(True)

class Reset:        
    def GET(self):
        print 'reset'
        plotter.reset()
        return json.dumps(True)


class Draw:        
    def GET(self, x, y):
        print 'draw to ' + x + ',' + y
        safety.stop()
        plotter.drawLineTo(Point(int(x),int(y)),Plotter.DWN)
        safety.start()
        return json.dumps(True)
    

if __name__ == "__main__":
    app.run()
