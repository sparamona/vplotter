from adafruit_motorkit import MotorKit

class Stepper:

  BACKWARD = 2
  
  def __init__(self,isLeft):
    kit = MotorKit()
    self._isLeft = isLeft
    if isLeft:
      self._stepper = kit.stepper2
    else:
      self._stepper = kit.stepper1

  def stepup(self):
    if self._isLeft:
      self._stepper.onestep()
    else:
      self._stepper.onestep(direction=self.BACKWARD, style=2)

  def stepdown(self):
    if self._isLeft:
      self._stepper.onestep(direction=self.BACKWARD)
    else:
      self._stepper.onestep()


