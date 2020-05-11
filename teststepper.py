from stepper import Stepper
import time
import RPi.GPIO as GPIO

# Stepper 1 >>> s = Stepper(16,15,17,27,14)
# Stepper 2 >>> s = Stepper(16,22,23,24,25)


#s1 = Stepper(16, 15,17,27,14)
s1 = Stepper(16, 15,17,27,14)
s2 = Stepper(16, 22,23,24,25)

def f(s,n,d,direct):
    for i in range(0,200*n):
        s.step(direct)
        time.sleep(d)

def c():
    GPIO.cleanup()
