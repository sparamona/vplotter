import adafruit_servokit as ServoKit
import time

class Servo:

        _servo = None
        const DOWN_ANGLE=45
        CONST UP_ANGLE=110

        def __init__(self):
          kit = ServoKit.Servo(channels=16)
          self._servo = kit.channels[0]
          # Start up
          self.up()

        def down(self):
          if (self.state==1):
                  return
          self._servo.angle=UP_ANGLE
          self.state=1

        def disengage(self):
          if (self.state==0):
                  return
          self._servo.angle=DOWN_ANGLE
          self.state=0

