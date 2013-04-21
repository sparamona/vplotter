import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
solenoid_pin = 27

class Solenoid:

  def __init__(self):
    GPIO.setup(solenoid_pin, GPIO.OUT)
    self.state = 0

  def engage(self):
    if (self.state==1):
      return
    GPIO.output(solenoid_pin,1)
    self.state=1

  def disengage(self):
    if (self.state==0):
      return
    time.delay(.3)
    GPIO.output(solenoid_pin,0)
    time.delay(.3)
    self.state=0

