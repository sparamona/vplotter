import adafruit_motorkit as MotorKit

class Stepper:

  _stepper = None
  
  def __init__(isLeft):
    self._kit = MotorKit()
    if isLeft:
      self._stepper = kit.stepper1
    else:
      self._stepper = kit.stepper2

  def stepup(self):
    self._stepper.onstep()


  def stepdown(self):
    self._stepper.onstep(direction=adafruit_motor.stepper.BACKWARD)

