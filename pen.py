from servo import Servo
from sys import argv

p=Servo()

if (argv[1]=="up"):
    p.up()
elif (argv[1]=="down"):
    p.down()
else:
    print("need argument <up|down>")

    
