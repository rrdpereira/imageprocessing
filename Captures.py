import sys, time, os, datetime
from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

import os, glob
import micasense.capture as capture
# %matplotlib inline

imagePath = os.path.join('.','data','0000SET','000')
imageNames = glob.glob(os.path.join(imagePath,'IMG_0000_*.tif'))

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