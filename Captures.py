#!/usr/bin/env python
# coding: utf-8

import sys, time, os, datetime, glob
import micasense.capture as capture

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

imageNames = glob.glob(os.path.join(imagePath,'IMG_0000_*.tif'))
print(imageNames)

capture = capture.Capture.from_filelist(imageNames)
print(capture.uuid)
capture.plot_raw(fig_size=(9,8),num=1)

VVersion='03'
outputPath = os.path.join(imagePath,VVersion,'stacks')
outputFilename = capture.uuid
fullOutputPath = os.path.join(outputPath, outputFilename)

capture.plot_vignette(fig_size=(9,8), num=2)

capture.plot_undistorted_radiance(fig_size=(9,8), num=3)

# capture.plot_undistorted_reflectance(fig_size=(9,8), num=4)

capture.plot_panels(fig_size=(9,8), num=5, color_bar=False)

# capture.save_bands_in_separate_file(fullOutputPath)