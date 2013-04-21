import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Solenoid:

  def __init(self):
    solenoid_pin = 27
    GPIO.setup(solenoid_pin, GPIO.OUT)
    self.state = 0

  def engage(self):
    if (self.state==1) return
    GPIO.output(solenoid_pin,1)
    self.state=1

  def disengage(self):
    if (self.state==0) return
    GPIO.output(solenoid_pin,0)
    self.state=0

