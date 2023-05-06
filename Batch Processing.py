#!/usr/bin/env python
# coding: utf-8

from ipywidgets import FloatProgress, Layout
from IPython.display import display
import micasense.imageset as imageset
import micasense.capture as capture
import os, glob
import multiprocessing

import sys, time, os, datetime
from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

DataIMG="IMG_0"
PlaqueIMG="IMG_0070_"
panelNames = None
useDLS = True

#RRDP
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdgeImageSet','0000SET'))
# panelNames = glob.glob(os.path.join(imagePath,'000','IMG_0000_*.tif'))
# panelCap = capture.Capture.from_filelist(panelNames)

#Linux filepath
#imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
#Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
imagePath = os.path.join('r:\\','proc_field','RedEdge3')

# imagePath = os.path.join('.','data','RedEdge3')
#imagePath = os.path.join('~','Downloads','RedEdge3')
# imageNames = glob.glob(os.path.join(imagePath,DataIMG+'**_*.tif'))
panelNames = glob.glob(os.path.join(imagePath,PlaqueIMG+'*.tif'))

print('imagePath: {0}'.format(imagePath))
print('panelNames: {0}'.format(panelNames))
# print(imageNames)

#RRPD
""" outputPath = os.path.join(imagePath,'..','stacks')
thumbnailPath = os.path.join(outputPath, '..', 'thumbnails') """
#RRPD
VVersion='03'
outputPath = os.path.join(imagePath,VVersion,'stacks')
thumbnailPath = os.path.join(outputPath,VVersion, 'thumbnails')

print('outputPath: {0}'.format(outputPath))
print('thumbnailPath: {0}'.format(thumbnailPath))

overwrite = False # can be set to set to False to continue interrupted processing
generateThumbnails = True

# Allow this code to align both radiance and reflectance images; bu excluding
# a definition for panelNames above, radiance images will be used
# For panel images, efforts will be made to automatically extract the panel information
# but if the panel/firmware is before Altum 1.3.5, RedEdge 5.1.7 the panel reflectance
# will need to be set in the panel_reflectance_by_band variable.
# Note: radiance images will not be used to properly create NDVI/NDRE images below.
if panelNames is not None:
    panelCap = capture.Capture.from_filelist(panelNames)
    print('panelCap: {0}'.format(panelCap))
    print('FlagA')
else:
    panelCap = None
    print('FlagB')

print('panelCap: {0}'.format(panelCap))

if panelCap is not None:
    print('Flag00')
    # if panelCap.panel_albedo() is not None:
    if panelCap.panel_albedo() is not None and not any(v is None for v in panelCap.panel_albedo()):
        panel_reflectance_by_band = panelCap.panel_albedo()
        print('len(panel_reflectance_by_band): {0}'.format(len(panel_reflectance_by_band)))
        print('panel_reflectance_by_band: {0}'.format(panel_reflectance_by_band))
        print('Flag01')
    else:
        #RRDP
        #raise IOError("Comment this lne and set panel_reflectance_by_band here")
        #RRDP
        #panel_reflectance_by_band = [0.55]*len(imageNames)
        panel_reflectance_by_band = [0.57, 0.57, 0.56, 0.51, 0.55] #RedEdge3 band_index order
        #RRDP
        #panel_reflectance_by_band = [0.67, 0.69, 0.68, 0.61, 0.67] #RedEdge band_index order
        print('len(panel_reflectance_by_band): {0}'.format(len(panel_reflectance_by_band)))
        print('panel_reflectance_by_band: {0}'.format(panel_reflectance_by_band))
        print('Flag02')
    
    panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)
    print('panel_irradiance: {0}'.format(panel_irradiance))
    img_type = "reflectance"
    print('Flag03')
else:
    if useDLS:
        img_type='reflectance'
        print('Flag04')
    else:
        img_type = "radiance"
        print('Flag05')