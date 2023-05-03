import numpy as np
import micasense.dls as dls

import os, glob
import micasense.capture as capture

import sys, time, os, datetime
from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

images_path = os.path.join('.','data','0000SET','000')
image_names = glob.glob(os.path.join(images_path,'IMG_0000_*.tif'))
cap = capture.Capture.from_filelist(image_names)
# set panel corners manually if zbar is not installed
panelCorners = [[[809,613],[648,615],[646,454],[808,452]],
                [[772,623],[613,625],[610,464],[770,462]],
                [[771,651],[611,653],[610,492],[770,490]],
                [[829,658],[668,659],[668,496],[829,496]],
                [[807,632],[648,634],[645,473],[805,471]]]

cap.set_panel_corners(panelCorners)

# Define DLS sensor orientation vector relative to dls pose frame
dls_orientation_vector = np.array([0,0,-1])
# compute sun orientation and sun-sensor angles
(
    sun_vector_ned,    # Solar vector in North-East-Down coordinates
    sensor_vector_ned, # DLS vector in North-East-Down coordinates
    sun_sensor_angle,  # Angle between DLS vector and sun vector
    solar_elevation,   # Elevation of the sun above the horizon
    solar_azimuth,     # Azimuth (heading) of the sun
) = dls.compute_sun_angle(cap.location(),
                      cap.dls_pose(),
                      cap.utc_time(),
                      dls_orientation_vector)

# Since the diffuser reflects more light at shallow angles than at steep angles,
# we compute a correction for this
fresnel_correction = dls.fresnel(sun_sensor_angle)

# Now we can correct the raw DLS readings and compute the irradiance on level ground
dls_irradiances = []
center_wavelengths = []
for img in cap.images:
    dir_dif_ratio = 6.0
    percent_diffuse = 1.0/dir_dif_ratio
    # measured Irradiance / fresnelCorrection
    sensor_irradiance = img.spectral_irradiance / fresnel_correction
    untilted_direct_irr = sensor_irradiance / (percent_diffuse + np.cos(sun_sensor_angle))
    # compute irradiance on the ground using the solar altitude angle
    dls_irr = untilted_direct_irr * (percent_diffuse + np.sin(solar_elevation))
    dls_irradiances.append(dls_irr)
    center_wavelengths.append(img.center_wavelength)

import matplotlib.pyplot as plt
plt.figure(figsize=(9,6.75),num=1)
plt.scatter(center_wavelengths,dls_irradiances)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Irradiance ($W/m^2/nm$)')
plt.show()

cap.plot_undistorted_reflectance(dls_irradiances,fig_size=(9,8),num=2)

import math

panel_reflectance_by_band = [0.67, 0.69, 0.68, 0.61, 0.67] #RedEdge band_index order

panel_radiances = np.array(cap.panel_radiance())
irr_from_panel = math.pi * panel_radiances / panel_reflectance_by_band
dls_correction = irr_from_panel/dls_irradiances
cap.plot_undistorted_reflectance(dls_irradiances*dls_correction,fig_size=(9,8),num=3)

plt.figure(figsize=(9,6.75),num=4)
plt.scatter(cap.center_wavelengths(), cap.panel_reflectance())
plt.title("Panel Reflectances")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.show()