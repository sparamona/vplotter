from adafruit_motorkit import MotorKit

class Stepper:

  _stepper = None
  BACKWARD = 2
  
  def __init__(self,isLeft):
    kit = MotorKit()
    if isLeft:
      self._stepper = kit.stepper1
    else:
      self._stepper = kit.stepper2

  def stepup(self):
    self._stepper.onestep()


  def stepdown(self):
    self._stepper.onestep(direction=self.BACKWARD)

