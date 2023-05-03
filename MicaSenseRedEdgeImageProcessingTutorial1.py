import cv2
import matplotlib.pyplot as plt
import numpy as np
import os,glob
import math

import sys, time, os, datetime
from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

imagePath = os.path.join('.','data','0000SET','000')
imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Read raw image DN values
# reads 16 bit tif - this will likely not work for 12 bit images
imageRaw=plt.imread(imageName)

# Display the image
fig, ax = plt.subplots(figsize=(9,6.75),num=1)
ax.imshow(imageRaw, cmap='gray')
plt.show()

import micasense.plotutils as plotutils

# Optional: pick a color map that fits your viewing style
# one of 'gray, viridis, plasma, inferno, magma, nipy_spectral'
plotutils.colormap('magma')

fig = plotutils.plotwithcolorbar(imageRaw, title='Raw image values with colorbar',num=2)

import micasense.metadata as metadata
exiftoolPath = None
if os.name == 'nt':
    exiftoolPath = os.environ.get('exiftoolpath')
# get image metadata
meta = metadata.Metadata(imageName, exiftoolPath=exiftoolPath)
# prompt command line:
# exiftool -s -ImageSize -ExposureTime -CentralWavelength -WavelengthFWHM -CaptureId -FlightId -FocalLength -BlackLevel -RadiometricCalibration -VignettingCenter -VignettingPolynomial -BitsPerSample .\IMG_0290_3.tif
cameraMake = meta.get_item('EXIF:Make')
cameraModel = meta.get_item('EXIF:Model')
firmwareVersion = meta.get_item('EXIF:Software')
bandName = meta.get_item('XMP:BandName')
print('{0} {1} firmware version: {2}'.format(cameraMake, 
                                             cameraModel, 
                                             firmwareVersion))
print('Exposure Time: {0} seconds'.format(meta.get_item('EXIF:ExposureTime')))
print('Imager Gain: {0}'.format(meta.get_item('EXIF:ISOSpeed')/100.0))
print('Size: {0}x{1} pixels'.format(meta.get_item('EXIF:ImageWidth'),meta.get_item('EXIF:ImageHeight')))
print('Band Name: {0}'.format(bandName))
print('Center Wavelength: {0} nm'.format(meta.get_item('XMP:CentralWavelength')))
print('Bandwidth: {0} nm'.format(meta.get_item('XMP:WavelengthFWHM')))
print('Capture ID: {0}'.format(meta.get_item('XMP:CaptureId')))
print('Flight ID: {0}'.format(meta.get_item('XMP:FlightId')))
print('Focal Length: {0}'.format(meta.get_item('XMP:FocalLength')))

import micasense.utils as msutils
radianceImage, L, V, R = msutils.raw_image_to_radiance(meta, imageRaw)
plotutils.plotwithcolorbar(V,'Vignette Factor',num=3)
plotutils.plotwithcolorbar(R,'Row Gradient Factor',num=4)
plotutils.plotwithcolorbar(V*R,'Combined Corrections',num=5)
plotutils.plotwithcolorbar(L,'Vignette and row gradient corrected raw values',num=6)
plotutils.plotwithcolorbar(radianceImage,'All factors applied and scaled to radiance',num=7)

markedImg = radianceImage.copy()
ulx = 660 # upper left column (x coordinate) of panel area
uly = 490 # upper left row (y coordinate) of panel area
lrx = 840 # lower right column (x coordinate) of panel area
lry = 670 # lower right row (y coordinate) of panel area
cv2.rectangle(markedImg,(ulx,uly),(lrx,lry),(0,255,0),3)

# Our panel calibration by band (from MicaSense for our specific panel)
panelCalibration = { 
    "Blue": 0.67, 
    "Green": 0.69, 
    "Red": 0.68, 
    "Red edge": 0.67, 
    "NIR": 0.61 
}

# Select panel region from radiance image
panelRegion = radianceImage[uly:lry, ulx:lrx]
plotutils.plotwithcolorbar(markedImg, 'Panel region in radiance image',num=8)
meanRadiance = panelRegion.mean()
print('Mean Radiance in panel region: {:1.3f} W/m^2/nm/sr'.format(meanRadiance))
panelReflectance = panelCalibration[bandName]
radianceToReflectance = panelReflectance / meanRadiance
print('Radiance to reflectance conversion factor: {:1.3f}'.format(radianceToReflectance))

reflectanceImage = radianceImage * radianceToReflectance
plotutils.plotwithcolorbar(reflectanceImage, 'Converted Reflectane Image',num=9)

panelRegionRaw = imageRaw[uly:lry, ulx:lrx]
panelRegionRefl = reflectanceImage[uly:lry, ulx:lrx]
panelRegionReflBlur = cv2.GaussianBlur(panelRegionRefl,(55,55),5)
plotutils.plotwithcolorbar(panelRegionReflBlur, 'Smoothed panel region in reflectance image',num=10)
print('Min Reflectance in panel region: {:1.2f}'.format(panelRegionRefl.min()))
print('Max Reflectance in panel region: {:1.2f}'.format(panelRegionRefl.max()))
print('Mean Reflectance in panel region: {:1.2f}'.format(panelRegionRefl.mean()))
print('Standard deviation in region: {:1.4f}'.format(panelRegionRefl.std()))

# correct for lens distortions to make straight lines straight
undistortedReflectance = msutils.correct_lens_distortion(meta, reflectanceImage)
plotutils.plotwithcolorbar(undistortedReflectance, 'Undistorted reflectance image',num=11)

flightImageName = os.path.join(imagePath,'IMG_0001_4.tif')
flightImageRaw=plt.imread(flightImageName)
plotutils.plotwithcolorbar(flightImageRaw, 'Raw Image',num=12)

flightRadianceImage, _, _, _ = msutils.raw_image_to_radiance(meta, flightImageRaw)
flightReflectanceImage = flightRadianceImage * radianceToReflectance
flightUndistortedReflectance = msutils.correct_lens_distortion(meta, flightReflectanceImage)
plotutils.plotwithcolorbar(flightUndistortedReflectance, 'Reflectance converted and undistorted image',num=13)