import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Stepper:

  def __init__(self,enable_pin,coil_A_1_pin,coil_A_2_pin,coil_B_1_pin,coil_B_2_pin):
    self.enable_pin=enable_pin
    self.coil_A_1_pin=coil_A_1_pin
    self.coil_A_2_pin=coil_A_2_pin
    self.coil_B_1_pin=coil_B_1_pin
    self.coil_B_2_pin=coil_B_2_pin

    GPIO.setup(enable_pin, GPIO.OUT)
    GPIO.setup(coil_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_B_2_pin, GPIO.OUT)

    GPIO.output(enable_pin, 1)
    self.STEPS = [ [1,0,1,0], [0,1,1,0], [0,1,0,1], [1,0,0,1] ]
    self.IDX = 0

  def step(self,direction):
    if (direction == 0):
      return
    self.IDX= (self.IDX + 1*direction) % 4
    self.setStep(self.STEPS[self.IDX])

  def stepup(self):
    self.IDX= (self.IDX + 1) % 4
    self.setStep(self.STEPS[self.IDX])

  def stepdown(self):
    self.IDX= (self.IDX - 1) % 4
    self.setStep(self.STEPS[self.IDX])

  def setStep(self,W):
    #print("step ", W)
    GPIO.output(self.coil_A_1_pin, W[0])
    GPIO.output(self.coil_A_2_pin, W[1])
    GPIO.output(self.coil_B_1_pin, W[2])
    GPIO.output(self.coil_B_2_pin, W[3])

#s = Stepper(18,4,17,23,24)
#while True:
#  delay = raw_input("Delay between steps (milliseconds)?")
#  steps = raw_input("How many steps forward? ")
#  s.forward(int(delay) / 1000.0, int(steps))
#  steps = raw_input("How many steps backwards? ")
#  s.backwards(int(delay) / 1000.0, int(steps))
