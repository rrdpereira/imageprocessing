#!/usr/bin/env python
# coding: utf-8

import sys, time, os, datetime, glob
from ipywidgets import FloatProgress, Layout
from IPython.display import display
import micasense.imageset as imageset
import pandas as pd
import math
import numpy as np
from mapboxgl.viz import *
from mapboxgl.utils import df_to_geojson, create_radius_stops, scale_between, create_color_stops 
import matplotlib.pyplot as plt

from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

## This progress widget is used for display of the long-running process
f = FloatProgress(min=0, max=1, layout=Layout(width='100%'), description="Loading")
display(f)
def update_f(val):
    if (val - f.value) > 0.005 or val == 1: #reduces cpu usage from updating the progressbar by 10x
        f.value=val

# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
imagePath = os.path.join('r:\\','proc_field','RedEdgeImageSet','0000SET')
print(imagePath)

panelNames = glob.glob(os.path.join(imagePath,'IMG_0002_*.tif'))
print(panelNames)

# %time imgset = imageset.ImageSet.from_directory(imagePath, progress_callback=update_f)
imgset = imageset.ImageSet.from_directory(imagePath, progress_callback=update_f)

data, columns = imgset.as_nested_lists()
print("Columns: {}".format(columns))
df = pd.DataFrame.from_records(data, index='timestamp', columns=columns)

#Insert your mapbox token here
token = 'pk.eyJ1IjoibWljYXNlbnNlIiwiYSI6ImNqYWx5dWNteTJ3cWYzMnBicmZid3g2YzcifQ.Zrq9t7GYocBtBzYyT3P4sw'
color_stops = create_color_stops(np.linspace(-math.pi,math.pi,num=8),colors='YlOrRd')
data = df_to_geojson(df,columns[3:],lat='latitude',lon='longitude')
viz = CircleViz(data, access_token=token, color_property='dls-yaw',
                color_stops=color_stops,
                center=[df['longitude'].median(),df['latitude'].median()], 
                zoom=16, height='600px',
                style='mapbox://styles/mapbox/satellite-streets-v9')
viz.show()
plt.figure(num=1)

# 'b' as blue |'g' as green | 'r' as red | 'c' as cyan | 'm' as magenta | 'y' as yellow | 'k' as black | 'w' as white
ax=df.plot(y=columns[3:], subplots=True, figsize=(15,6.75), style=['g','c','y','k','b','g','r','k','m'])
for a in ax:
    a.legend(loc='right', bbox_to_anchor=(1.1, 0.5), ncol=1, fancybox=True, shadow=True)
plt.show()
plt.close()

plt.figure(num=3)
# plot the histogram of the altitude data
df.altitude.hist()
# find the altitude above which the flight images occur
cutoff_altitude = df.altitude.mean()-3.0*df.altitude.std()
plt.axvline(x=cutoff_altitude,c='r')
plt.xlabel('Capture altitude (m)')
plt.ylabel('Number of occurances')
plt.show()
plt.close()

flight = df.altitude>cutoff_altitude
ground = ~flight
ground_idx = np.arange(len(ground))[ground]
flight_idx = np.arange(len(ground))[flight]
ground_captures = np.array(imgset.captures)[ground_idx]
flight_captures = np.array(imgset.captures)[flight_idx]

panel_radiances = []
dls_irradiances = []
panel_timestamps = []
for cap in ground_captures:
    if cap.panels_in_all_expected_images():
        panel_timestamps.append(cap.utc_time())
        panel_radiances.append(cap.panel_radiance())
        dls_irradiances.append(cap.dls_irradiance())

dls_irradiances = np.asarray(dls_irradiances)
panel_radiances = np.asarray(panel_radiances)

panel_reflectance_by_band = [0.67, 0.69, 0.68, 0.61, 0.67] #RedEdge band_index order
panel_irradiance = ground_captures[0].panel_irradiance(panel_reflectance_by_band)
plt.figure(num=4)
plt.scatter(ground_captures[0].center_wavelengths(), panel_irradiance)
plt.xscale('log')
plt.ylabel("Irradiance (w/m^2/nm)")
plt.xlabel("Wavelength (nm)")
plt.show()
plt.close()
plt.figure(num=4)

# 'b' as blue |'g' as green | 'r' as red | 'c' as cyan | 'm' as magenta | 'y' as yellow | 'k' as black | 'w' as white
df[df.altitude>cutoff_altitude].plot(y=columns[8:13], figsize=(14,8), style=['b','g','r','k','m'],)
plt.ylabel("Irradiance (w/m^2/nm)")
plt.show()
plt.close()