#!/usr/bin/env python
# coding: utf-8

import os, glob
import micasense.capture as capture
from micasense.image import Image
from micasense.panel import Panel
import cv2
import numpy as np
import matplotlib.pyplot as plt
import micasense.imageutils as imageutils
import micasense.plotutils as plotutils
from micasense import plotutils
import matplotlib.pyplot as plt
import imageio
from osgeo import gdal, gdal_array

panelNames = None
paneCap = None

""" imagePath = os.path.join('.','data','10BANDSET','000')
imageNames = glob.glob(os.path.join(imagePath,'IMG_0431_*.tif'))
panelNames = glob.glob(os.path.join(imagePath,'IMG_0000_*.tif')) """

#Linux filepath
#imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
#Windows filepath
imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
imageNames = glob.glob(os.path.join(imagePath,'IMG_0309_*.tif'))
panelNames = glob.glob(os.path.join(imagePath,'IMG_00**_*.tif'))

# Allow this code to align both radiance and reflectance images; bu excluding
# a definition for panelNames above, radiance images will be used
# For panel images, efforts will be made to automatically extract the panel information
# but if the panel/firmware is before Altum 1.3.5, RedEdge 5.1.7 the panel reflectance
# will need to be set in the panel_reflectance_by_band variable.
# Note: radiance images will not be used to properly create NDVI/NDRE images below.
if panelNames is not None:
    panelCap = capture.Capture.from_filelist(panelNames)
else:
    panelCap = None

capture = capture.Capture.from_filelist(imageNames)

if panelCap is not None:
    if panelCap.panel_albedo() is not None:
        panel_reflectance_by_band = panelCap.panel_albedo()
    else:
        #raise IOError("Comment this lne and set panel_reflectance_by_band here")
        panel_reflectance_by_band = [0.55]*len(imageNames)
    panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)    
    img_type = "reflectance"
    capture.plot_undistorted_reflectance(panel_irradiance)
else:
    if capture.dls_present():
        img_type='reflectance'
        capture.plot_undistorted_reflectance(capture.dls_irradiance())
    else:
        img_type = "radiance"
        capture.plot_undistorted_radiance() 

## Alignment settings
match_index = 4 # Index of the band, here we use green
max_alignment_iterations = 20
warp_mode = cv2.MOTION_HOMOGRAPHY # MOTION_HOMOGRAPHY or MOTION_AFFINE. For Altum images only use HOMOGRAPHY
pyramid_levels = 3 # for 10-band imagery we use a 3-level pyramid. In some cases

print("Alinging images. Depending on settings this can take from a few seconds to many minutes")
# Can potentially increase max_iterations for better results, but longer runtimes
warp_matrices, alignment_pairs = imageutils.align_capture(capture,
                                                          ref_index = match_index,
                                                          max_iterations = max_alignment_iterations,
                                                          warp_mode = warp_mode,
                                                          pyramid_levels = pyramid_levels)

print("Finished Aligning, warp matrices={}".format(warp_matrices))

cropped_dimensions, edges = imageutils.find_crop_bounds(capture, warp_matrices, warp_mode=warp_mode)
im_aligned = imageutils.aligned_capture(capture, warp_matrices, warp_mode, cropped_dimensions, match_index, img_type=img_type)

# figsize=(30,23) # use this size for full-image-resolution display
figsize=(16,13)   # use this size for export-sized display

#rgb_band_indices = [capture.band_names().index('Red'),capture.band_names().index('Green'),capture.band_names().index('Blue-444')]
rgb_band_indices = [capture.band_names().index('Red'),capture.band_names().index('Green'),capture.band_names().index('Blue')]
#cir_band_indices = [capture.band_names().index('NIR'),capture.band_names().index('Red'),capture.band_names().index('Green')]
cir_band_indices = [capture.band_names().index('Red'),capture.band_names().index('NIR'),capture.band_names().index('Green')]

# Create a normalized stack for viewing
im_display = np.zeros((im_aligned.shape[0],im_aligned.shape[1],im_aligned.shape[2]), dtype=np.float32 )

im_min = np.percentile(im_aligned[:,:,rgb_band_indices].flatten(), 0.5)  # modify these percentiles to adjust contrast
im_max = np.percentile(im_aligned[:,:,rgb_band_indices].flatten(), 99.5)  # for many images, 0.5 and 99.5 are good values

# for rgb true color, we use the same min and max scaling across the 3 bands to 
# maintain the "white balance" of the calibrated image
for i in rgb_band_indices:
    im_display[:,:,i] =  imageutils.normalize(im_aligned[:,:,i], im_min, im_max)

rgb = im_display[:,:,rgb_band_indices]

# for cir false color imagery, we normalize the NIR,R,G bands within themselves, which provides
# the classical CIR rendering where plants are red and soil takes on a blue tint
for i in cir_band_indices:
    im_display[:,:,i] =  imageutils.normalize(im_aligned[:,:,i])

cir = im_display[:,:,cir_band_indices]
fig, axes = plt.subplots(1, 2, figsize=figsize)
axes[0].set_title("Red-Green-Blue Composite")
axes[0].imshow(rgb)
axes[1].set_title("Color Infrared (CIR) Composite")
axes[1].imshow(cir)
plt.show()

# Create an enhanced version of the RGB render using an unsharp mask
gaussian_rgb = cv2.GaussianBlur(rgb, (9,9), 10.0)
gaussian_rgb[gaussian_rgb<0] = 0
gaussian_rgb[gaussian_rgb>1] = 1
unsharp_rgb = cv2.addWeighted(rgb, 1.5, gaussian_rgb, -0.5, 0)
unsharp_rgb[unsharp_rgb<0] = 0
unsharp_rgb[unsharp_rgb>1] = 1

# Apply a gamma correction to make the render appear closer to what our eyes would see
gamma = 1.4
gamma_corr_rgb = unsharp_rgb**(1.0/gamma)
fig = plt.figure(figsize=figsize)
plt.imshow(gamma_corr_rgb, aspect='equal')
plt.axis('off')
plt.show()

imtype = 'png' # or 'jpg'
imageio.imwrite('rgb.'+imtype, (255*gamma_corr_rgb).astype('uint8'))
imageio.imwrite('cir.'+imtype, (255*cir).astype('uint8'))

rows, cols, bands = im_display.shape
driver = gdal.GetDriverByName('GTiff')
filename = "bbggrreeen" #blue,blue,green,green,red,red,rededge,rededge,rededge,nir

sort_by_wavelength = True # set to false if you want stacks in camera-band-index order
    
outRaster = driver.Create(filename+".tiff", cols, rows, bands, gdal.GDT_UInt16, options = [ 'INTERLEAVE=BAND','COMPRESS=DEFLATE' ])
try:
    if outRaster is None:
        raise IOError("could not load gdal GeoTiff driver")

    if sort_by_wavelength:
        eo_list = list(np.argsort(capture.center_wavelengths()))
    else:
        eo_list = capture.eo_indices()

    for outband,inband in enumerate(eo_list):
        outband = outRaster.GetRasterBand(outband+1)
        outdata = im_aligned[:,:,inband]
        outdata[outdata<0] = 0
        outdata[outdata>2] = 2   #limit reflectance data to 200% to allow some specular reflections
        outband.WriteArray(outdata*32768) # scale reflectance images so 100% = 32768
        outband.FlushCache()

    for outband,inband in enumerate(capture.lw_indices()):
        outband = outRaster.GetRasterBand(len(eo_list)+outband+1)
        outdata = (im_aligned[:,:,inband]+273.15) * 100 # scale data from float degC to back to centi-Kelvin to fit into uint16
        outdata[outdata<0] = 0
        outdata[outdata>65535] = 65535
        outband.WriteArray(outdata)
        outband.FlushCache()
finally:
    outRaster = None

nir_band = [name.lower() for name in capture.band_names()].index('nir')
red_band = [name.lower() for name in capture.band_names()].index('red')

np.seterr(divide='ignore', invalid='ignore') # ignore divide by zero errors in the index calculation

# Compute Normalized Difference Vegetation Index (NDVI) from the NIR(3) and RED (2) bands
ndvi = (im_aligned[:,:,nir_band] - im_aligned[:,:,red_band]) / (im_aligned[:,:,nir_band] + im_aligned[:,:,red_band])

# remove shadowed areas (mask pixels with NIR reflectance < 20%))
if img_type == 'reflectance':
    ndvi = np.ma.masked_where(im_aligned[:,:,nir_band] < 0.20, ndvi) 
elif img_type == 'radiance':
    lower_pct_radiance = np.percentile(im_aligned[:,:,3],  10.0)
    ndvi = np.ma.masked_where(im_aligned[:,:,nir_band] < lower_pct_radiance, ndvi) 
    
# Compute and display a histogram
ndvi_hist_min = np.min(ndvi)
ndvi_hist_max = np.max(ndvi)
fig, axis = plt.subplots(1, 1, figsize=(10,4))
axis.hist(ndvi.ravel(), bins=512, range=(ndvi_hist_min, ndvi_hist_max))
plt.title("NDVI Histogram")
plt.show()

min_display_ndvi = 0.45 # further mask soil by removing low-ndvi values
#min_display_ndvi = np.percentile(ndvi.flatten(),  5.0)  # modify with these percentilse to adjust contrast
max_display_ndvi = np.percentile(ndvi.flatten(), 99.5)  # for many images, 0.5 and 99.5 are good values
masked_ndvi = np.ma.masked_where(ndvi < min_display_ndvi, ndvi)

#reduce the figure size to account for colorbar
figsize=np.asarray(figsize) - np.array([3,2])

#plot NDVI over an RGB basemap, with a colorbar showing the NDVI scale
fig, axis = plotutils.plot_overlay_withcolorbar(gamma_corr_rgb, 
                                    masked_ndvi, 
                                    figsize = figsize, 
                                    title = 'NDVI filtered to only plants over RGB base layer',
                                    vmin = min_display_ndvi,
                                    vmax = max_display_ndvi)
fig.savefig('ndvi_over_rgb.png')

# Compute Normalized Difference Red Edge Index from the NIR(3) and RedEdge(4) bands
rededge_band = [name.lower() for name in capture.band_names()].index('red edge')
ndre = (im_aligned[:,:,nir_band] - im_aligned[:,:,rededge_band]) / (im_aligned[:,:,nir_band] + im_aligned[:,:,rededge_band])

# Mask areas with shadows and low NDVI to remove soil
masked_ndre = np.ma.masked_where(ndvi < min_display_ndvi, ndre)

# Compute a histogram
ndre_hist_min = np.min(masked_ndre)
ndre_hist_max = np.max(masked_ndre)
fig, axis = plt.subplots(1, 1, figsize=(10,4))
axis.hist(masked_ndre.ravel(), bins=512, range=(ndre_hist_min, ndre_hist_max))
plt.title("NDRE Histogram (filtered to only plants)")
plt.show()

min_display_ndre = np.percentile(masked_ndre, 5)
max_display_ndre = np.percentile(masked_ndre, 99.5)

fig, axis = plotutils.plot_overlay_withcolorbar(gamma_corr_rgb, 
                                    masked_ndre, 
                                    figsize=figsize, 
                                    title='NDRE filtered to only plants over RGB base layer',
                                    vmin=min_display_ndre,vmax=max_display_ndre)
fig.savefig('ndre_over_rgb.png')

x_band = red_band
y_band = nir_band
x_max = np.max(im_aligned[:,:,x_band])
y_max = np.max(im_aligned[:,:,y_band])

fig = plt.figure(figsize=(12,12))
plt.hexbin(im_aligned[:,:,x_band],im_aligned[:,:,y_band],gridsize=640,bins='log',extent=(0,x_max,0,y_max))
ax = fig.gca()
ax.set_xlim([0,x_max])
ax.set_ylim([0,y_max])
plt.xlabel("{} Reflectance".format(capture.band_names()[x_band]))
plt.ylabel("{} Reflectance".format(capture.band_names()[y_band]))
plt.show()

print(warp_matrices)