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
PlaqueIMG="IMG_0071_"
panelNames = None
useDLS = True

#Linux filepath
#imagePath = os.path.expanduser(os.path.join('~','Downloads','DualCam-Farm','farm_only'))
#Windows filepath
imagePath = os.path.join('r:\\','proc_field','DualCam-Farm','farm_only')
panelNames = glob.glob(os.path.join(imagePath,'IMG_0002_*.tif'))

print('imagePath: {0}'.format(imagePath))
print('panelNames: {0}'.format(panelNames))

outputPath = os.path.join(imagePath,'..','stacks')
thumbnailPath = os.path.join(outputPath, '..', 'thumbnails')

print('outputPath: {0}'.format(outputPath))
print('thumbnailPath: {0}'.format(thumbnailPath))

overwrite = False # Set to False to continue interrupted processing
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
    if panelCap.panel_albedo() is not None:
        panel_reflectance_by_band = panelCap.panel_albedo()
        print('len(panel_reflectance_by_band): {0}'.format(len(panel_reflectance_by_band)))
        print('panel_reflectance_by_band: {0}'.format(panel_reflectance_by_band))
        print('Flag01')
    else:
        panel_reflectance_by_band = [0.65]*len(panelCap.images) #inexact, but quick
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
df = pd.DataFrame.from_records(data, index='timestamp', columns=columns)

#Insert your mapbox token here
token = 'pk.eyJ1IjoibWljYXNlbnNlIiwiYSI6ImNqYWx5dWNteTJ3cWYzMnBicmZid3g2YzcifQ.Zrq9t7GYocBtBzYyT3P4sw'
color_property = 'dls-yaw'
color_property = 'altitude'
num_color_classes = 8

min_val = df[color_property].min()
max_val = df[color_property].max()

#RRDP
# breaks = jenkspy.jenks_breaks(df[color_property], nb_class=num_color_classes)
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

# Use the warp_matrices derived from the Alignment Tutorial for this RedEdge set without RigRelatives
warp_matrices = [array([[ 1.0020243e+00, -3.7388311e-04,  2.4971788e+01],
       [ 6.7297497e-04,  1.0005866e+00,  1.7188536e+01],
       [ 2.4259109e-06, -9.2373267e-07,  1.0000000e+00]], dtype=float32), array([[ 9.9140632e-01, -4.6332614e-05,  4.8500401e+01],
       [ 3.2340995e-05,  9.9200422e-01, -1.0915921e+01],
       [-7.3704086e-07,  5.0890253e-07,  1.0000000e+00]], dtype=float32), array([[ 1.0018263e+00, -2.1731904e-04,  5.5316315e+00],
       [ 7.2411756e-04,  1.0021795e+00,  5.8745198e+00],
       [-1.9047379e-08,  9.7758209e-07,  1.0000000e+00]], dtype=float32), array([[ 9.9152303e-01, -5.4825414e-03,  4.1536880e+01],
       [ 3.8441001e-03,  9.9495757e-01,  1.7250452e+01],
       [-3.2921032e-06, -2.4233820e-08,  1.0000000e+00]], dtype=float32), array([[ 1.0006192e+00, -3.0658240e-04, -2.5816131e-01],
       [ 7.8755329e-05,  9.9954307e-01,  2.9809377e-01],
       [ 9.1640561e-07, -1.0784843e-06,  1.0000000e+00]], dtype=float32), array([[ 9.9773926e-01, -6.3800282e-04,  5.2199936e+01],
       [-3.4246168e-03,  9.9601907e-01,  2.0550659e+01],
       [-4.6251063e-07, -4.8716843e-06,  1.0000000e+00]], dtype=float32), array([[ 9.9622118e-01,  3.1637053e-03,  3.7498917e+01],
       [-6.7951437e-03,  9.9743211e-01,  8.9517927e+00],
       [-3.6472218e-06, -2.4649705e-06,  1.0000000e+00]], dtype=float32), array([[ 9.8943901e-01,  3.7658634e-04,  9.4948044e+00],
       [-4.0384033e-03,  9.8851675e-01,  1.5366467e+01],
       [-2.4371677e-06, -3.8438825e-06,  1.0000000e+00]], dtype=float32), array([[ 9.9749213e-01,  1.6272087e-03,  4.3243721e-01],
       [-7.3282972e-05,  9.9533182e-01,  3.5523354e+01],
       [ 3.8597086e-06, -4.0187538e-07,  1.0000000e+00]], dtype=float32), array([[ 9.9992698e-01,  6.6664284e-03, -9.0784521e+00],
       [-9.0053231e-03,  9.9836856e-01,  1.5190173e+01],
       [-1.6761204e-07, -3.6131762e-06,  1.0000000e+00]], dtype=float32)]

use_multi_process = True # set to False for single-process saving
overwrite_existing = False # skip existing files, set to True to overwrite

## This progress widget is used for display of the long-running process
f2 = FloatProgress(min=0, max=1, layout=Layout(width='100%'), description="Saving")
display(f2)
def update_f2(val):
    f2.value=val

#RRDP
if not os.path.exists(outputPath):
    os.makedirs(outputPath)
if generateThumbnails and not os.path.exists(thumbnailPath):
    os.makedirs(thumbnailPath)

# Save out geojson data so we can open the image capture locations in our GIS
with open(os.path.join(outputPath,'imageSet.json'),'w') as f:
    f.write(str(geojson_data))

# If we didn't provide a panel above, irradiance set to None will cause DLS data to be used
try:
    irradiance = panel_irradiance+[0]
except NameError:
    irradiance = None

#RRDP
#start_time = datetime.datetime.now()
start = datetime.datetime.now()

#RRDP
# Save all captures in the imageset as aligned stacks
""" imgset.save_stacks(warp_matrices,
                     outputPath,
                     thumbnailPath,
                     irradiance = irradiance,
                     multiprocess=use_multi_process, 
                     overwrite=overwrite_existing, 
                     progress_callback=update_f2)

end_time = datetime.datetime.now()
update_f2(1.0) """

#RRDP
for i,capture in enumerate(imgset.captures):
    outputFilename = capture.uuid+'.tif'
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
            capture.save_capture_as_stack(fullOutputPath)
            if generateThumbnails:
                capture.save_capture_as_rgb(fullThumbnailPath)
    capture.clear_image_data()
    update_f2(float(i)/float(len(imgset.captures)))
update_f2(1.0)
end = datetime.datetime.now()

#RRDP
#print("Saving time: {}".format(end_time-start_time))
print("Saving time: {}".format(end-start))

#RRDP
#print("Alignment+Saving rate: {:.2f} captures per second".format(float(len(imgset.captures))/float((end_time-start_time).total_seconds())))
print("Alignment+Saving rate: {:.2f} captures per second".format(float(len(imgset.captures))/float((end-start).total_seconds())))

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

lines = [header]
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
if(subprocess.check_call(cmd) == 0):
    print("Successfully updated stack metadata")