from adafruit_servokit import ServoKit
import time

class Servo:

        _servo = None
        state=1
        DOWN_ANGLE=60
        UP_ANGLE=50

        def __init__(self):
          kit = ServoKit(channels=16)
          self._servo = kit.servo[0]
          # Start up
          self.up()

        def down(self):
          if (self.state==1):
                  return
          self._servo.angle=self.DOWN_ANGLE
          self.state=1
          time.sleep(0.1)

        def up(self):
          if (self.state==0):
                  return
          self._servo.angle=self.UP_ANGLE
          self.state=0

