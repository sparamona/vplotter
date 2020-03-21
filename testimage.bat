python3 .\Img2PlotXY.py %1 .\images\intermediate-xy.plot %2 %3 %4 %5
set OUTFILE=%1-out-_%2_%3_%4_%5.png
python3 .\Plot2Img.py .\images\intermediate-xy.plot %OUTFILE%
%OUTFILE%

