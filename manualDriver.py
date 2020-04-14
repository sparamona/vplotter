import driver2
from Plotter import Lengths,Point,Plotter
import io
import driver2

plotfile = io.BytesIO()
plotter  = Plotter(plotfile)
driver = driver2.BuildDriver(plotfile)

while True:
    print("Plotter at: " + str(driver.pointFromLengths(driver.currentLengths)))
    x,y = input("Draw to: ").split()
    plotfile.truncate()
    plotter.drawLineTo(Point(float(x),float(y)),False)
    plotfile.seek(0)
    print("running driver")
    driver.run()
    print("complete.")




