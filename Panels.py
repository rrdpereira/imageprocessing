import os, glob
from micasense.image import Image
from micasense.panel import Panel
import matplotlib.pyplot as plt

import sys, time, os, datetime
from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

#Linux filepath
#imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
#Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
imagePath = os.path.join('r:\\','proc_field','RedEdge3')

# imagePath = os.path.join('.','data','RedEdge3')
#imagePath = os.path.join('.','Users','rpereira','Documents','IMAmt_Sorriso','2020','05.29.2020-IMA_Sorriso','RedEdge','05cm_11h')
#imagePath = os.path('C:\\Users\\rpereira\\Documents\\IMAmt_Sorriso\\2020\\05.29.2020-IMA_Sorriso\\RedEdge\\05cm_11h')
print(imagePath)
#imageName = glob.glob(os.path.join(imagePath,'IMG_0000_1.tif'))[0]
# imageName = glob.glob(os.path.join(imagePath,'IMG_00**_*.tif'))[0]
imageName = glob.glob(os.path.join(imagePath,'IMG_006*_1.tif'))[0]
print(imageName)

img = Image(imageName)
if img.auto_calibration_image:
    print("Found automatic calibration image")
panel = Panel(img)

if not panel.panel_detected():
    raise IOError("Panel Not Detected!")
    
print("Detected panel serial: {}".format(panel.serial))
mean, std, num, sat_count = panel.raw()
print("Extracted Panel Statistics:")
print("Mean: {}".format(mean))
print("Standard Deviation: {}".format(std))
print("Panel Pixel Count: {}".format(num))
print("Saturated Pixel Count: {}".format(sat_count))

panel.plot(figsize=(9,6.75),num=1)
# #initialize belief
# mu = [0.0, 0.0, 0.0]
# sigma = np.array([[1.0, 0.0, 0.0],\
#                     [0.0, 1.0, 0.0],\
#                     [0.0, 0.0, 1.0]])

# map_limits = [-1, 12, -1, 10]
#   
# plt.figure(figsize=(8,8),num=1)
# plt.grid()
# plt.axis(map_limits)
# plt.ylabel("y[m]")
# plt.xlabel("x[m]")
# plt.title("Mobile Robot estimated POSITIONS by EFK", loc = "center")
# plt.savefig("FigP00_EKFrouteXY.png", format = "png", dpi = 300)
# plt.show()

imagePath = os.path.join('.','data','0000SET','000')
print(imagePath)
imageName = glob.glob(os.path.join(imagePath,'IMG_0000_1.tif'))[0]
print(imageName)

img = Image(imageName)
panel = Panel(img)

if not panel.panel_detected():
    raise IOError("Panel Not Detected!")
    
print("Detected panel serial: {}".format(panel.serial))
mean, std, num, sat_count = panel.raw()
print("Extracted Panel Statistics:")
print("Mean: {}".format(mean))
print("Standard Deviation: {}".format(std))
print("Panel Pixel Count: {}".format(num))
print("Saturated Pixel Count: {}".format(sat_count))

panel.plot(figsize=(9,6.75),num=2)
# #initialize belief
# mu = [0.0, 0.0, 0.0]
# sigma = np.array([[1.0, 0.0, 0.0],\
#                     [0.0, 1.0, 0.0],\
#                     [0.0, 0.0, 1.0]])

# map_limits = [-1, 12, -1, 10]
#   
# plt.figure(figsize=(8,8),num=1)
# plt.grid()
# plt.axis(map_limits)
# plt.ylabel("y[m]")
# plt.xlabel("x[m]")
# plt.title("Mobile Robot estimated POSITIONS by EFK", loc = "center")
# plt.savefig("FigP00_EKFrouteXY.png", format = "png", dpi = 300)
# plt.show()