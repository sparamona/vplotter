python3 .\Img2PlotXY.py .\images\test1.jpg .\images\test1-xy.plot %1 %2 %3 %4
set OUTFILE=.\images\output_%1_%2_%3_%4.png
python3 .\Plot2Img.py .\images\test1-xy.plot %OUTFILE%
%OUTFILE%

