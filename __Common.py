#!/usr/bin/env python
# coding: utf-8

**********************************************************************************************************************************

import sys, time, os, datetime, glob
from micasense.image import Image
from micasense.panel import Panel
import matplotlib.pyplot as plt


--------------------------------------

import sys, time, os, datetime, glob
from micasense.image import Image
from micasense.panel import Panel
import cv2 #openCV
import exiftool
import os, glob
import numpy as np
import pyzbar.pyzbar as pyzbar
import mapboxgl
import matplotlib.pyplot as plt

--------------------------------------
import sys, time, os, datetime, glob
import micasense.plotutils as plotutils
import micasense.metadata as metadata
import micasense.utils as msutils
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

--------------------------------------

import sys, time, os, datetime, glob
import micasense.image as image
import micasense.panel as panel
import micasense.capture as capture
import micasense.imageset as imageset
from ipywidgets import FloatProgress
from IPython.display import display
import matplotlib.pyplot as plt

--------------------------------------

import sys, time, os, datetime, glob
import micasense.dls as dls
import micasense.capture as capture
import numpy as np
import math
import matplotlib.pyplot as plt

--------------------------------------

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

--------------------------------------

import sys, time, os, datetime, glob
from micasense.image import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

--------------------------------------

import sys, time, os, datetime, glob
import cv2
import argparse
import numpy as np
from matplotlib import pyplot as plt

--------------------------------------

import sys, time, os, datetime, glob
import micasense.metadata as metadata
import micasense.capture as capture
import micasense.imageset as imageset
import micasense.utils as msutils
import micasense.plotutils as plotutils
import micasense.panel as panel
import micasense.dls as dls
from micasense.image import Image
import cv2
from PIL import Image as Img
import numpy as np
import subprocess
import math
from ipywidgets import FloatProgress, Layout
from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt

--------------------------------------

import sys, time, os, datetime, glob
import micasense.capture as capture

--------------------------------------

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

--------------------------------------

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

--------------------------------------

import sys, time, os, datetime, glob
import micasense.imageutils as imageutils
import micasense.plotutils as plotutils
import micasense.capture as capture
from micasense import plotutils
import cv2
import numpy as np
import imageio
from osgeo import gdal, gdal_array
import matplotlib.pyplot as plt
%matplotlib inline

--------------------------------------

import sys, time, os, datetime, glob
import micasense.capture as capture
import micasense.imageutils as imageutils
import micasense.plotutils as plotutils
from micasense import plotutils
import cv2
import numpy as np
import imageio
from osgeo import gdal, gdal_array
import matplotlib.pyplot as plt


--------------------------------------

import sys, time, os, datetime, glob
import micasense.capture as capture
import micasense.imageutils as imageutils
import micasense.plotutils as plotutils
from micasense import plotutils
from micasense.image import Image
from micasense.panel import Panel
import cv2
import numpy as np
import imageio
from osgeo import gdal, gdal_array
import matplotlib.pyplot as plt


**********************************************************************************************************************************
Notebook

%load_ext autoreload
%autoreload 2

After Libs
%matplotlib inline

**********************************************************************************************************************************

from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

**********************************************************************************************************************************

imagePath = os.path.join('.','data','0000SET','000')
imageName = os.path.join(imagePath,'IMG_0000_4.tif')

image_path = os.path.join('.','data','0000SET','000','IMG_0000_1.tif')
img = image.Image(image_path)

**********************************************************************************************************************************
# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
imagePath = os.path.join('r:\\','proc_field','RedEdge3')
print(imagePath)

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

# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
# imagePath = os.path.join('r:\\','proc_field','RedEdge3')
imagePath = os.path.join('.','data','0000SET','000')
print(imagePath)

imageName = glob.glob(os.path.join(imagePath,'IMG_0000_1.tif'))[0]
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

panel.plot(figsize=(9,6.75),num=2)

# Method 01
# imagePath = os.path.join('.','data','0000SET','000')
# imageName = os.path.join(imagePath,'IMG_0000_4.tif')

# Method 02
# Linux filepath
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
# Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
# imagePath = os.path.join('r:\\','proc_field','RedEdge3')
imagePath = os.path.join('.','data','ALTUM1SET','000')
print(imagePath)

imageName = glob.glob(os.path.join(imagePath,'IMG_0000_1.tif'))[0]
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

panel.plot(figsize=(9,6.75),num=3)

--------------------------------------
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

--------------------------------------

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

**********************************************************************************************************************************
