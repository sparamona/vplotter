from Plotter import Lengths,Point,Plotter
import driver3
import io,sys

plotfile = io.BytesIO()
driver = driver3.BuildDriver(plotfile)

print("Plotter at: " + str(driver.currentLengths))
origin = driver.pointFromLengths(driver.currentLengths)
x = float(sys.argv[1])
y = float(sys.argv[2])
#x,y = input("Draw to (from 0,0): ").split()
#a,b = input("New lengths: ").split()
#driver.moveTo(Lengths(float(a),float(b)))
driver.drawLineTo(Point(origin.x+float(x),origin.y+float(y)),False)
#driver.reset()
plotfile.seek(0)

driver.run()
print("complete.")




