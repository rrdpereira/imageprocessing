#!/usr/bin/env python
# coding: utf-8

import sys, time, os, datetime, glob
import micasense.image as image
import micasense.panel as panel
import micasense.capture as capture
import micasense.imageset as imageset
from ipywidgets import FloatProgress
from IPython.display import display
import matplotlib.pyplot as plt

from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
imagePath = os.path.join('.','data','0000SET','000')
print(imagePath)

imageName = glob.glob(os.path.join(imagePath,'IMG_0000_4.tif'))[0]
print(imageName)

image_path = os.path.join('.','data','0000SET','000','IMG_0000_1.tif')

img = image.Image(image_path)

img.plot_raw(figsize=(9,6.75),num=1)

print('{0} {1} firmware version: {2}'.format(img.meta.camera_make(),
                                             img.meta.camera_model(), 
                                             img.meta.firmware_version()))
print('Exposure Time: {0} seconds'.format(img.meta.exposure()))
print('Imager Gain: {0}'.format(img.meta.gain()))
print('Size: {0}x{1} pixels'.format(img.meta.image_size()[0],
                                    img.meta.image_size()[1]))
print('Band Name: {0}'.format(img.meta.band_name()))
print('Center Wavelength: {0} nm'.format(img.meta.center_wavelength()))
print('Bandwidth: {0} nm'.format(img.meta.bandwidth()))
print('Capture ID: {0}'.format(img.meta.capture_id()))
print('Flight ID: {0}'.format(img.meta.flight_id()))

# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
images_path = os.path.join('.','data','0000SET','000')
print(images_path)

image_names = glob.glob(os.path.join(images_path,'IMG_0000_*.tif'))
print(image_names)

cap = capture.Capture.from_filelist(image_names)
# cap.plot_radiance(fig_size=(9,6.75),num=2)
cap.plot_radiance(fig_size=(9,8),num=2)

print(cap.band_names())
fig = plt.figure(figsize=(14,6),num=3)
plt.subplot(1,2,1)
plt.scatter(cap.center_wavelengths(), cap.dls_irradiance())
plt.ylabel('Irradiance $(W/m^2/nm)$')
plt.xlabel('Center Wavelength (nm)')
plt.subplot(1,2,2)
plt.scatter(cap.band_names(), [img.meta.exposure() for img in cap.images])
plt.xlabel('Band Names')
plt.ylim([0,2.5e-3])
plt.ylabel('Exposure Time (s)')
plt.show()

# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
image_path = os.path.join('.','data','0000SET','000','IMG_0000_1.tif')
print(image_path)

img = image.Image(image_path)
# panelCorners - if we dont have zbar installed to scan the QR codes, detect panel manually and 
panelCorners = [[[809,613],[648,615],[646,454],[808,452]],
                [[772,623],[613,625],[610,464],[770,462]],
                [[771,651],[611,653],[610,492],[770,490]],
                [[829,658],[668,659],[668,496],[829,496]],
                [[807,632],[648,634],[645,473],[805,471]]]
print(panelCorners)
print()
print(panelCorners[0])
print()
pnl = panel.Panel(img,panelCorners = panelCorners[0])
print("Panel found: {}".format(pnl.panel_detected()))
print("Panel serial: {}".format(pnl.serial))
print("QR Code Corners:\n{}".format(pnl.qr_corners()))
mean, std, count, saturated_count = pnl.raw()
print("Panel mean raw pixel value: {}".format(mean))
print("Panel raw pixel standard deviation: {}".format(std))
print("Panel region pixel count: {}".format(count))
print("Panel region saturated pixel count: {}".format(count))

pnl.plot(figsize=(9,6.75),num=4)

f = FloatProgress(min=0, max=1)
display(f)
def update_f(val):
    f.value=val


# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')
images_dir = os.path.join('.','data','0000SET')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
print(images_dir)

imgset = imageset.ImageSet.from_directory(images_dir, progress_callback=update_f)

for cap in imgset.captures:
    print ("Opened Capture {} with bands {}".format(cap.uuid,[str(band) for band in cap.band_names()]))