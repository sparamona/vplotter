import time

class Solenoid:

  def __init__(self):
    self.state = 0

  def engage(self):
    if (self.state==1):
      return
    print "solenoid engaged"
    self.state=1

  def disengage(self):
    if (self.state==0):
      return
    print "solenoid disengaged"
    self.state=0

