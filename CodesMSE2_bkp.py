#!/usr/bin/env python
# coding: utf-8

#kullanımı: 
#1- ReflectanceImagesFolder ve images_path konumları belirlenmeli
#2- panel corners belirlenmeli ve matriste  image koordinantları yazılmalı
#3- band index değerleri kontrol edilmeli(bu kısım önemli) #-*-coding:utf-8-*-

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
import micasense.panel as panel

PlaqueIMG="IMG_0071_"
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
ReflectanceImagesFolder = os.path.join('r:\\','proc_field','RedEdge3','OUT3')

#RRDP
#Linux filepath
#images_path = os.path.join('.','data','RedEdge3') 
#images_path = os.path.join(r'C:\Users\emre\Desktop\aaa')             # Path part of raw images will be written in this part
#Windows filepath
# images_path = os.path.join('c:\\','Users','robso','Downloads','RedEdge3')
images_path = os.path.join('r:\\','proc_field','RedEdge3')

# ReflectanceImagesFolder = os.path.join('.','data','RedEdge3','OUT')
# images_path = os.path.join('.','data','RedEdge3')
# image_names = glob.glob(os.path.join(images_path, 'IMG_0063_*.tif'))
image_names = glob.glob(os.path.join(images_path, PlaqueIMG+'*.tif'))

print(ReflectanceImagesFolder)
print(images_path)
print(image_names)

cap = capture.Capture.from_filelist(image_names)
print(cap)
print('CAP: {0}'.format(cap))
cap.plot_raw()

# img = Image(os.path.join('r:\\','proc_field','RedEdge3','IMG_0063_1.tif'))
img = Image(os.path.join('r:\\','proc_field','RedEdge3',PlaqueIMG+'1.tif'))

# RRDP panelCorners to panel_corners
# panel_corners = [[[800, 1090], [645, 11084], [651, 941], [797, 949]],
#                 [[921, 1110], [775, 1085], [789, 952], [927, 958]],
#                 [[921, 1012], [771, 1002], [776, 866], [926, 859]],
#                 [[802, 1035], [666, 1005], [664, 872], [794, 875]],
#                 [[865, 1077], [727, 1049], [716, 910], [858, 913]],
#                 [[194, 211], [150, 211], [195, 182], [220, 180]]]

# panel_corners = [[[110, 410], [100, 410], [100, 400], [110, 400]]]
panel_corners = [[[610, 540], [600, 540], [600, 530], [610, 530]]]

print(panel_corners)
print()
print(panel_corners[0])
print()
pnl = panel.Panel(img,panelCorners = panel_corners[0])
print("Panel found: {}".format(pnl.panel_detected()))
print("Panel serial: {}".format(pnl.serial))
print("QR Code Corners:\n{}".format(pnl.qr_corners()))
mean, std, count, saturated_count = pnl.raw()
print("Panel mean raw pixel value: {}".format(mean))
print("Panel raw pixel standard deviation: {}".format(std))
print("Panel region pixel count: {}".format(count))
print("Panel region saturated pixel count: {}".format(count))

imgNB = os.path.join('r:\\','proc_field','RedEdge3')
print('imgNB: {0}'.format(imgNB))
# imgPNB = glob.glob(os.path.join(imgNB,'IMG_0063_4.tif'))[0]
imgPNB = glob.glob(os.path.join(imgNB,PlaqueIMG+'4.tif'))[0]

imgB = Image(imgPNB)
imgB.plot_all(figsize=(9,6.75),num=1)

pnl.plot(figsize=(9,6.75),num=4)
# RRDP
# cap.set_panelCorners(panelCorners)
cap.set_panel_corners(panel_corners)

#doğrulanmış DLS2 okumaları - ground seviyesinde
dls_irradiances = []
center_wavelengths = []
for img in cap.images:

    dls_irr = img.horizontal_irradiance
    dls_irradiances.append(dls_irr)
    center_wavelengths.append(img.center_wavelength)

plt.figure(figsize=(9,6.75),num=1)
plt.scatter(center_wavelengths, dls_irradiances)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Irradiance ($W/m^2/nm$)')
plt.show()
plt.close()

#cap.plot_undistorted_reflectance(dls_irradiances)
cap.plot_undistorted_reflectance(dls_irradiances,fig_size=(9,8),num=2)

# panel_reflectance_by_band = [0.519, 0.521, 0.52, 0.518, 0.519]  # Altum band_index
panel_reflectance_by_band = [0.57, 0.57, 0.56, 0.50, 0.55]  # RedEdge3 band_index

panel_radiances = np.array(cap.panel_radiance())
irr_from_panel = math.pi * panel_radiances / panel_reflectance_by_band
dls_correction = irr_from_panel / dls_irradiances
cap.plot_undistorted_reflectance(dls_irradiances * dls_correction,fig_size=(9,8),num=3)

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
            #plotutils.plotwithcolorbar(Reflectance, 'Reflektans görüntüsü')
            print("Band ok1-Blue")

        if band == "Green":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_green)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflektans görüntüsü')
            print("Band ok2-Green")

        if band == "Red":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_red)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflektans görüntüsü')
            print("Band ok3-Red")

        if band == "NIR":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_nir)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflektans görüntüsü')
            print("Band ok4-NIR")

        if band == "Red edge":
            Reflectance = img.undistorted_reflectance(dls_irr* dls_correction_redEdge)
            #plotutils.plotwithcolorbar(Reflectance, 'Reflektans görüntüsü')
            print("Band ok5-RedEdge")

        outfile = os.path.join(ReflectanceImagesFolder,filename)
        print(outfile)
        im = Img.fromarray(Reflectance)
        with open(outfile, 'w') as img: #create CSV
            im.save(os.path.join(outfile),format= 'tiff')##123
            print("Save image")

    if os.environ.get('exiftoolpath') is not None:
        exiftool_cmd = os.path.normpath(os.environ.get('exiftoolpath'))
    else:
        exiftool_cmd = 'exiftool'
        
    cmd = 'exiftool -tagsFromFile "{}" -ALL -XMP {}'.format(file, figname)
    print(cmd)
#RRDP
#subprocess.check_call(cmd)
    if(subprocess.check_call(cmd) == 0):
        print("Successfully updated stack metadata")

        subprocess.run(['exiftool', '-tagsFromFile', file, '-ALL', '-XMP', figname])
        print("Exiftool 1")

        subprocess.run(['exiftool', '-delete_original!', figname])
        print("Exiftool OK")