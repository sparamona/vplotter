import matplotlib.pyplot as plt
import numpy as np
from PIL import Image 
import sys
  
img = Image.open(sys.argv[1]).convert("L")
_ = plt.hist(img.getdata(), bins='auto')
plt.show()