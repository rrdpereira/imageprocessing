from micasense.image import Image
import os, glob
# %matplotlib inline

import sys, time, os, datetime
from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

imagePath = os.path.join('.','data','0000SET','000')
imageName = glob.glob(os.path.join(imagePath,'IMG_0000_1.tif'))[0]

img = Image(imageName)
img.plot_all(figsize=(9,6.75),num=1)

import numpy as np
import matplotlib.pyplot as plt
import cv2

nbins = 1024
vmin = 0
vmax = 2**16
bins = range(vmin,vmax, int(vmax/nbins))
hist = cv2.calcHist([img.raw().ravel()],[0],None,[nbins],[vmin,vmax])
plt.figure(figsize=(9,6.75),num=2)
plt.plot(bins,hist)
plt.xlim(img.raw().min(),img.raw().max())
plt.ylim(0,hist.max())
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.show()
plt.close()