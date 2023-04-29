import os
import micasense.image as image
#%matplotlib inline

image_path = os.path.join('.','data','0000SET','000','IMG_0000_1.tif')
img = image.Image(image_path)
img.plot_raw();

print('{0} {1} firmware version: {2}'.format(img.meta.camera_make(),
                                             img.meta.camera_model(), 
                                             img.meta.firmware_version()))
print('Exposure Time: {0} seconds'.format(img.meta.exposure()))
print('Imager Gain: {0}'.format(img.meta.gain()))
print('Size: {0}x{1} pixels'.format(img.meta.image_size()[0],
                                    img.meta.image_size()[1]))
print('Band Name: {0}'.format(img.meta.band_name()))
print('Center Wavelength: {0} nm'.format(img.meta.center_wavelength()))
print('Bandwidth: {0} nm'.format(img.meta.bandwidth()))
print('Capture ID: {0}'.format(img.meta.capture_id()))
print('Flight ID: {0}'.format(img.meta.flight_id()))

import os, glob
import micasense.capture as capture

images_path = os.path.join('.','data','0000SET','000')
image_names = glob.glob(os.path.join(images_path,'IMG_0000_*.tif'))
cap = capture.Capture.from_filelist(image_names)
cap.plot_radiance();

import matplotlib.pyplot as plt

print(cap.band_names())
fig = plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
plt.scatter(cap.center_wavelengths(), cap.dls_irradiance())
plt.ylabel('Irradiance $(W/m^2/nm)$')
plt.xlabel('Center Wavelength (nm)')
plt.subplot(1,2,2)
plt.scatter(cap.band_names(), [img.meta.exposure() for img in cap.images])
plt.xlabel('Band Names')
plt.ylim([0,2.5e-3])
plt.ylabel('Exposure Time (s)')
plt.show()

import os, glob
import micasense.image as image
import micasense.panel as panel

image_path = os.path.join('.','data','0000SET','000','IMG_0000_1.tif')
img = image.Image(image_path)
# panelCorners - if we dont have zbar installed to scan the QR codes, detect panel manually and 
panelCorners = [[[809,613],[648,615],[646,454],[808,452]],
                [[772,623],[613,625],[610,464],[770,462]],
                [[771,651],[611,653],[610,492],[770,490]],
                [[829,658],[668,659],[668,496],[829,496]],
                [[807,632],[648,634],[645,473],[805,471]]]
print(panelCorners)
print()
print(panelCorners[0])
print()
pnl = panel.Panel(img,panelCorners = panelCorners[0])
print("Panel found: {}".format(pnl.panel_detected()))
print("Panel serial: {}".format(pnl.serial))
print("QR Code Corners:\n{}".format(pnl.qr_corners()))
mean, std, count, saturated_count = pnl.raw()
print("Panel mean raw pixel value: {}".format(mean))
print("Panel raw pixel standard deviation: {}".format(std))
print("Panel region pixel count: {}".format(count))
print("Panel region saturated pixel count: {}".format(count))

pnl.plot();

from ipywidgets import FloatProgress
from IPython.display import display
f = FloatProgress(min=0, max=1)
display(f)
def update_f(val):
    f.value=val

import micasense.imageset as imageset
import os
images_dir = os.path.join('.','data','0000SET')

imgset = imageset.ImageSet.from_directory(images_dir, progress_callback=update_f)

for cap in imgset.captures:
    print ("Opened Capture {} with bands {}".format(cap.uuid,[str(band) for band in cap.band_names()]))