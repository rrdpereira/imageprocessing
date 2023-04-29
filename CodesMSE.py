#!/usr/bin/env python
# coding: utf-8

import micasense.metadata as metadata
from PIL import Image as Img
import numpy as np
import micasense.dls as dls
import os, glob
import micasense.capture as capture
import math
import matplotlib.pyplot as plt
from micasense.image import Image
import micasense.imageset as imageset
import micasense.utils as msutils
import micasense.plotutils as plotutils 
import subprocess

#RRDP
#Linux filepath
#imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
#Windows filepath
# imagePath = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')

#Linux filepath
# ReflectanceImagesFolder = os.path.join('.','data','RedEdge3','OUT')
#ReflectanceImagesFolder = (r'C:\Users\emre\Desktop\aaa\REF')         # The location of the files to be recorded will be determined
#Windows filepath
#ReflectanceImagesFolder = os.path.join('c:\\','Users','robso','Downloads','RedEdge3','OUT')
ReflectanceImagesFolder = os.path.join('r:\\','proc_field','RedEdge3','OUT')

#RRDP
#Linux filepath
#images_path = os.path.join('.','data','RedEdge3') 
#images_path = os.path.join(r'C:\Users\emre\Desktop\aaa')             # Path part of raw images will be written in this part
#Windows filepath
# images_path = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
images_path = os.path.join('r:\\','proc_field','RedEdge3')

#RRDP
image_names = glob.glob(os.path.join(images_path,'IMG_0309_*.tif'))
#image_names = glob.glob(os.path.join(images_path, 'IMG_0033_*.tif'))

#RRDP
panelNames = glob.glob(os.path.join(images_path,'IMG_00**_*.tif'))

#cap = capture.Capture.from_filelist(image_names)

#cap.plot_raw()

if panelNames is not None:
    cap = capture.Capture.from_filelist(panelNames)
else:
    cap = None

cap = capture.Capture.from_filelist(image_names)

if cap is not None:
    if cap.panel_albedo() is not None:
        panel_reflectance_by_band = cap.panel_albedo()
    else:
        #RRDP
        #raise IOError("Comment this lne and set panel_reflectance_by_band here")
        #RRDP
        #panel_reflectance_by_band = [0.55]*len(imageNames)
        panel_reflectance_by_band = [0.57, 0.57, 0.56, 0.51, 0.55] #RedEdge3 band_index order
    panel_irradiance = cap.panel_irradiance(panel_reflectance_by_band)    
    img_type = "reflectance"
    cap.plot_undistorted_reflectance(panel_irradiance)
else:
    if cap.dls_present():
        img_type='reflectance'
        cap.plot_undistorted_reflectance(cap.dls_irradiance())
    else:
        img_type = "radiance"
        cap.plot_undistorted_radiance()   
#panelCorners = [[[800, 1090], [645, 11084], [651, 941], [797, 949]],
 #               [[921, 1110], [775, 1085], [789, 952], [927, 958]],
  #              [[921, 1012], [771, 1002], [776, 866], [926, 859]],
   #             [[802, 1035], [666, 1005], [664, 872], [794, 875]],
    #            [[865, 1077], [727, 1049], [716, 910], [858, 913]]]



#cap.set_panelCorners(panelCorners)

#verified DLS2 readings - at ground level
dls_irradiances = []
center_wavelengths = []
for img in cap.images:

    dls_irr = img.horizontal_irradiance
    dls_irradiances.append(dls_irr)
    center_wavelengths.append(img.center_wavelength)



plt.scatter(center_wavelengths, dls_irradiances)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Irradiance ($W/m^2/nm$)')
plt.show()

cap.plot_undistorted_reflectance(dls_irradiances)

#panel_reflectance_by_band = [0.519, 0.521, 0.52, 0.518, 0.519]  # Altum band_index values

panel_radiances = np.array(cap.panel_radiance())
irr_from_panel = math.pi * panel_radiances / panel_reflectance_by_band
dls_correction = irr_from_panel / dls_irradiances
cap.plot_undistorted_reflectance(dls_irradiances * dls_correction)




channels = ['*.tif']

def band_adi(image):
    
    meta = metadata.Metadata(image)
    band = meta.get_item('XMP:BandName')
    return band

dls_correction_blue = (dls_correction[0])
dls_correction_green = (dls_correction[1])
dls_correction_red = dls_correction[2]
dls_correction_nir = dls_correction[3]
dls_correction_redEdge = dls_correction[4]


center_wavelengths=[]

for channel in channels:
    files= glob.glob(os.path.join(images_path,'*'+ channel + '*'))
    for file in files:
        img = Image(file)
        band = band_adi(file)
        cap = capture.Capture.from_file(file)
        dls_irr = img.horizontal_irradiance
        meta = metadata.Metadata(file)
        center_wavelengths.append(img.center_wavelength)

        if file.endswith(".tif"):
            figname = file[:-4] + '_reflectance.tif'
            print("figname", figname)


        path, filename = os.path.split(file)
         
        if band == "Blue":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_blue)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflectance image')


            print("operation ok-Blue")

        if band == "Green":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_green)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflectance image')
            print("operation ok2-Green")


        if band == "Red":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_red)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflectance image')

            print("operation ok3-Red")


        if band == "NIR":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_nir)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflectance image')

            print("operation ok4-NIR")

        if band == "Red edge":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_redEdge)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflectance image')

            print("operation ok5-RedEdge")

        if band == "LWIR":
            Reflectance = img.undistorted_reflectance()
            #plotutils.plotwithcolorbar(Reflectance, 'Reflectance image')

            print("operation ok6-Termal")
     
        outfile = os.path.join(ReflectanceImagesFolder ,filename )
        im = Img.fromarray(Reflectance)
        im.save(os.path.join(outfile,figname),format= 'tiff')##123
       
        

        subprocess.run(['exiftool', '-tagsFromFile', file, '-ALL', '-XMP', figname])
        subprocess.run(['exiftool', '-delete_original!', figname])

        print("registration is ok")