#!/usr/bin/env python
# coding: utf-8

import sys, time, os, datetime, glob
import micasense.imageset as imageset
import micasense.capture as capture
from ipywidgets import FloatProgress, Layout
from IPython.display import display
import multiprocessing
import subprocess
import math
import numpy as np
from numpy import array
from numpy import float32
from mapboxgl.viz import *
from mapboxgl.utils import df_to_geojson, create_radius_stops, scale_between
from mapboxgl.utils import create_color_stops
import pandas as pd
import jenkspy #RRDP
import exiftool

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
# print('imageNames: {0}'.format(imageNames))

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

## This progress widget is used for display of the long-running process
f = FloatProgress(min=0, max=1, layout=Layout(width='100%'), description="Loading")
display(f)
def update_f(val):
    if (val - f.value) > 0.005 or val == 1: #reduces cpu usage from updating the progressbar by 10x
        f.value=val

imgset = imageset.ImageSet.from_directory(imagePath, progress_callback=update_f)
update_f(1.0)

data, columns = imgset.as_nested_lists()
# data, columns = imageset.as_nested_lists()
df = pd.DataFrame.from_records(data, index='timestamp', columns=columns)

#Insert your mapbox token here
token = 'pk.eyJ1IjoibWljYXNlbnNlIiwiYSI6ImNqYWx5dWNteTJ3cWYzMnBicmZid3g2YzcifQ.Zrq9t7GYocBtBzYyT3P4sw'
color_property = 'dls-yaw'
num_color_classes = 8

min_val = df[color_property].min()
max_val = df[color_property].max()

#RRDP
breaks = jenkspy.jenks_breaks(df[color_property], n_classes=num_color_classes)

#RRDP
color_stops = create_color_stops(breaks,colors='YlOrRd')
geojson_data = df_to_geojson(df,columns[3:],lat='latitude',lon='longitude')

viz = CircleViz(geojson_data, access_token=token, color_property=color_property,
#RRDP
                color_stops=color_stops,
                center=[df['longitude'].median(),df['latitude'].median()], 
                zoom=16, height='600px',
                style='mapbox://styles/mapbox/satellite-streets-v9')
viz.show()

# Set warp_matrices to none to align using RigRelatives
# Or
# Use the warp_matrices derived from the Alignment Tutorial for this RedEdge set without RigRelatives

#RRDP
""" warp_matrices = [array([[ 1.0022864e+00, -2.5218755e-03, -7.8898020e+00],
       [ 2.3614739e-03,  1.0036649e+00, -1.3134377e+01],
       [-1.7785899e-06,  1.1343118e-06,  1.0000000e+00]], dtype=float32), array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]], dtype=float32), array([[ 9.9724638e-01, -1.5535230e-03,  1.2301294e+00],
       [ 8.6745428e-04,  9.9738181e-01, -1.6499169e+00],
       [-8.2816513e-07, -3.4488804e-07,  1.0000000e+00]], dtype=float32), array([[ 1.0007139e+00, -8.4427800e-03,  1.6312805e+01],
       [ 6.2834378e-03,  9.9977130e-01, -1.6011697e+00],
       [-1.9520389e-06, -6.3762940e-07,  1.0000000e+00]], dtype=float32), array([[ 9.9284178e-01,  9.2155562e-04,  1.6069822e+01],
       [-3.2895457e-03,  9.9262553e-01, -5.0333548e-01],
       [-1.5845577e-06, -1.7680986e-06,  1.0000000e+00]], dtype=float32)] """

warp_matrices = [array([[ 1.0016431e+00, -1.0885171e-03,  1.4502928e+01],
       [-8.7003410e-03,  9.8970139e-01,  3.0994341e+01],
       [ 1.0731413e-05, -9.2477812e-06,  1.0000000e+00]], dtype=float32), array([[ 1.0004344e+00, -1.9012572e-03, -1.4149743e+01],
       [-4.8677209e-03,  9.8928565e-01, -2.8596885e+00],
       [ 1.4022728e-05, -6.3364282e-06,  1.0000000e+00]], dtype=float32), array([[ 1.0085055e+00,  1.8316660e-03, -1.0653937e+01],
       [-2.1676912e-03,  1.0018681e+00, -4.5603695e+00],
       [ 1.2178871e-05,  1.7743813e-06,  1.0000000e+00]], dtype=float32), array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]], dtype=float32), array([[ 9.9842864e-01,  3.0990106e-03, -9.6143999e+00],
       [-2.9161605e-03,  9.9383956e-01,  9.7156782e+00],
       [ 4.7046042e-06, -2.9739924e-06,  1.0000000e+00]], dtype=float32)]

## This progress widget is used for display of the long-running process
f2 = FloatProgress(min=0, max=1, layout=Layout(width='100%'), description="Saving")
display(f2)
def update_f2(val):
    f2.value=val

if not os.path.exists(outputPath):
    os.makedirs(outputPath)
if generateThumbnails and not os.path.exists(thumbnailPath):
    os.makedirs(thumbnailPath)

# Save out geojson data so we can open the image capture locations in our GIS
with open(os.path.join(outputPath,'imageSet.json'),'w') as f:
    f.write(str(geojson_data))
    
try:
    irradiance = panel_irradiance+[0]
except NameError:
    irradiance = None

start = datetime.datetime.now()
for i,capture in enumerate(imgset.captures):
    #RRDP
    outputFilename = capture.uuid
    #outputFilename = capture.uuid+'.tif'
    #outputFilename = capture.uuid+'_'+str(capture.band_index)+'.tif'
    print(outputFilename)
    thumbnailFilename = capture.uuid+'.jpg'
    print(thumbnailFilename)
    fullOutputPath = os.path.join(outputPath, outputFilename)
    print(fullOutputPath)
    fullThumbnailPath= os.path.join(thumbnailPath, thumbnailFilename)
    print(fullThumbnailPath)
    if (not os.path.exists(fullOutputPath)) or overwrite:
        if(len(capture.images) == len(imgset.captures[0].images)):
            capture.create_aligned_capture(irradiance_list=irradiance, warp_matrices=warp_matrices)
            #RRDP
            #capture.save_capture_as_stack(fullOutputPath)
            #capture.save_bands_in_separate_file(fullOutputPath)
            capture.save_bands_in_separate_file(fullOutputPath)
            if generateThumbnails:
                capture.save_capture_as_rgb(fullThumbnailPath)
    capture.clear_image_data()
    update_f2(float(i)/float(len(imgset.captures)))
update_f2(1.0)
end = datetime.datetime.now()

print("Saving time: {}".format(end-start))
print("Alignment+Saving rate: {:.2f} images per second".format(float(len(imgset.captures))/float((end-start).total_seconds())))

def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

header = "SourceFile,\
GPSDateStamp,GPSTimeStamp,\
GPSLatitude,GpsLatitudeRef,\
GPSLongitude,GPSLongitudeRef,\
GPSAltitude,GPSAltitudeRef,\
FocalLength,\
XResolution,YResolution,ResolutionUnits\n"

#RRDP
""" lines = [header]
for capture in imgset.captures:
    #get lat,lon,alt,time
    outputFilename = capture.uuid+'.tif'
    fullOutputPath = os.path.join(outputPath, outputFilename)
    lat,lon,alt = capture.location()
    #write to csv in format:
    # IMG_0199_1.tif,"33 deg 32' 9.73"" N","111 deg 51' 1.41"" W",526 m Above Sea Level
    latdeg, latmin, latsec = decdeg2dms(lat)
    londeg, lonmin, lonsec = decdeg2dms(lon)
    latdir = 'North'
    if latdeg < 0:
        latdeg = -latdeg
        latdir = 'South'
    londir = 'East'
    if londeg < 0:
        londeg = -londeg
        londir = 'West'
    resolution = capture.images[0].focal_plane_resolution_px_per_mm

    linestr = '"{}",'.format(fullOutputPath)
    linestr += capture.utc_time().strftime("%Y:%m:%d,%H:%M:%S,")
    linestr += '"{:d} deg {:d}\' {:.2f}"" {}",{},'.format(int(latdeg),int(latmin),latsec,latdir[0],latdir)
    linestr += '"{:d} deg {:d}\' {:.2f}"" {}",{},{:.1f} m Above Sea Level,Above Sea Level,'.format(int(londeg),int(lonmin),lonsec,londir[0],londir,alt)
    linestr += '{}'.format(capture.images[0].focal_length)
    linestr += '{},{},mm'.format(resolution,resolution)
    linestr += '\n' # when writing in text mode, the write command will convert to os.linesep
    lines.append(linestr) """

lines = [header]
for i in range(0,5):
    band_number=str(i+1)
    for capture in imgset.captures:
        #get lat,lon,alt,time
        outputFilename = capture.uuid+'_'+band_number+'.tif'
        fullOutputPath = os.path.join(outputPath, outputFilename)
        lat,lon,alt = capture.location()
        #write to csv in format:
        # IMG_0199_1.tif,"33 deg 32' 9.73"" N","111 deg 51' 1.41"" W",526 m Above Sea Level
        latdeg, latmin, latsec = decdeg2dms(lat)
        londeg, lonmin, lonsec = decdeg2dms(lon)
        latdir = 'North'
        if latdeg < 0:
            latdeg = -latdeg
            latdir = 'South'
        londir = 'East'
        if londeg < 0:
            londeg = -londeg
            londir = 'West'
        resolution = capture.images[0].focal_plane_resolution_px_per_mm

        linestr = '"{}",'.format(fullOutputPath)
        linestr += capture.utc_time().strftime("%Y:%m:%d,%H:%M:%S,")
        linestr += '"{:d} deg {:d}\' {:.2f}"" {}",{},'.format(int(latdeg),int(latmin),latsec,latdir[0],latdir)
        linestr += '"{:d} deg {:d}\' {:.2f}"" {}",{},{:.1f} m Above Sea Level,Above Sea Level,'.format(int(londeg),int(lonmin),lonsec,londir[0],londir,alt)
        linestr += '{}'.format(capture.images[0].focal_length)
        linestr += '{},{},mm'.format(resolution,resolution)
        linestr += '\n' # when writing in text mode, the write command will convert to os.linesep
        lines.append(linestr)

fullCsvPath = os.path.join(outputPath,'log.csv')
print(outputPath)
print(fullCsvPath)
with open(fullCsvPath, 'w') as csvfile: #create CSV
    csvfile.writelines(lines)

if os.environ.get('exiftoolpath') is not None:
    exiftool_cmd = os.path.normpath(os.environ.get('exiftoolpath'))
else:
    exiftool_cmd = 'exiftool'
        
cmd = '{} -csv="{}" -overwrite_original {}'.format(exiftool_cmd, fullCsvPath, outputPath)
print(cmd)
#RRDP
#subprocess.check_call(cmd)
if(subprocess.check_call(cmd) == 0):
    print("Successfully updated stack metadata")