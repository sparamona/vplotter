import driver2
from Plotter import Lengths,Point,Plotter
import driver2
import io

plotfile = io.BytesIO()
driver = driver2.BuildDriver(plotfile)

print("Plotter at: " + str(driver.currentLengths))
#x,y = input("Draw to: ").split()
a,b = input("New lengths: ").split()
driver.moveTo(Lengths(float(a),float(b)))
plotfile.seek(0)
driver.run()
print("complete.")




