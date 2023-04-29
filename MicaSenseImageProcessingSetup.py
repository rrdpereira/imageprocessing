import cv2 #openCV
import exiftool
import os, glob
import numpy as np
import pyzbar.pyzbar as pyzbar
import matplotlib.pyplot as plt
import mapboxgl

print()
print("Successfully imported all required libraries.")
print()

if os.name == 'nt':
    if os.environ.get('exiftoolpath') is None:
        print("Set the `exiftoolpath` environment variable as described above")
    else:
        if not os.path.isfile(os.environ.get('exiftoolpath')):
            print("The provided exiftoolpath isn't a file, check the settings")

try:
    with exiftool.ExifTool(os.environ.get('exiftoolpath')) as exift:
        print('Successfully executed exiftool.')
except Exception as e:
    print("Exiftool isn't working. Double check that you've followed the instructions above.")
    print("The execption text below may help to find the source of the problem:")
    print()
    print(e)

from micasense.image import Image
imagePath = os.path.join('.','data','0000SET','000')
print(imagePath)
imageName = glob.glob(os.path.join(imagePath,'IMG_0000_1.tif'))[0]
print(imageName)

img = Image(imageName)
img.plot_raw(figsize=(8.73,8.73));
#plt.figure(1)

from micasense.panel import Panel
panel = Panel(img)
if not panel.panel_detected():
    raise IOError("Panel Not Detected! Check your installation of pyzbar")
else:
    #plt.figure(2)
    panel.plot(figsize=(8,8));

print('Success! Now you are ready for Part 1 of the tutorial.')