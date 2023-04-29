panelNames = None
paneCap = None

# RRDP
""" imagePath = os.path.join('.','data','10BANDSET','000')
imageNames = glob.glob(os.path.join(imagePath,'IMG_0431_*.tif'))
panelNames = glob.glob(os.path.join(imagePath,'IMG_0000_*.tif')) """

imagePath = os.path.join('.','data','RedEdge3')
imageNames = glob.glob(os.path.join(imagePath,'IMG_0309_*.tif'))
panelNames = glob.glob(os.path.join(imagePath,'IMG_00**_*.tif'))

#RRDP
print(imagePath)
print(imageNames)
print(panelNames)

#RRDP
""" outputPath = os.path.join(imagePath,'..','stacks')
thumbnailPath = os.path.join(outputPath, '..', 'thumbnails') """

outputPath = os.path.join(imagePath,'stacks')
thumbnailPath = os.path.join(outputPath, 'thumbnails')

#RRDP
print(outputPath)
print(thumbnailPath)


capture = capture.Capture.from_filelist(imageNames)

if panelCap is not None:
    if panelCap.panel_albedo() is not None:
        panel_reflectance_by_band = panelCap.panel_albedo()
    else:
        #RRDP
        #raise IOError("Comment this lne and set panel_reflectance_by_band here")
        #RRDP
        #panel_reflectance_by_band = [0.55]*len(imageNames)
        panel_reflectance_by_band = [0.57, 0.57, 0.56, 0.51, 0.55] #RedEdge3 band_index order
    panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)    
    img_type = "reflectance"
    capture.plot_undistorted_reflectance(panel_irradiance)

## Alignment settings
#RRDP
match_index = 3 # Index of the band, here we use green
#RRDP
max_alignment_iterations = 30
#RRDP
warp_mode = cv2.MOTION_HOMOGRAPHY # MOTION_HOMOGRAPHY or MOTION_AFFINE. For Altum images only use HOMOGRAPHY
#RRDP
pyramid_levels = 2 # for 10-band imagery we use a 3-level pyramid. In some cases

# figsize=(30,23) # use this size for full-image-resolution display
figsize=(16,13)   # use this size for export-sized display

#RRDP
#rgb_band_indices = [capture.band_names().index('Red'),capture.band_names().index('Green'),capture.band_names().index('Blue-444')]
rgb_band_indices = [capture.band_names().index('Red'),capture.band_names().index('Green'),capture.band_names().index('Blue')]
#cir_band_indices = [capture.band_names().index('NIR'),capture.band_names().index('Red'),capture.band_names().index('Green')]
cir_band_indices = [capture.band_names().index('Red'),capture.band_names().index('NIR'),capture.band_names().index('Green')]


#RedEdge3 warp_matrices
warp_matrices=[array([[ 1.0016431e+00, -1.0885171e-03,  1.4502928e+01],
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

VzUQ1NDQYSKO3nlOtpWm.tif


import subprocess
import exiftool

if os.environ.get('exiftoolpath') is not None:
    exiftool_cmd = os.path.normpath(os.environ.get('exiftoolpath'))
else:
    exiftool_cmd = 'exiftool'
    print(exiftool_cmd)
    print(fullCsvPath)
    print(outputPath)

#RRDP        
#cmd = '{} -csv="{}" -overwrite_original {}'.format(exiftool_cmd, fullCsvPath, outputPath)
cmd = str(exiftool_cmd)+" -csv="+str(fullCsvPath)+" -overwrite_original "+str(outputPath)
print(cmd)
#RRDP
subprocess.check_call(str(cmd))
""" if(subprocess.check_call(cmd) == 0):
    print("Successfully updated stack metadata") """

exiftool
./data/RedEdge3/stacks/log.csv
./data/RedEdge3/stacks
exiftool -csv=./data/RedEdge3/stacks/log.csv -overwrite_original ./data/RedEdge3/stacks
---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
<ipython-input-26-59ee9e579b13> in <module>
     15 print(cmd)
     16 #RRDP
---> 17 subprocess.check_call(str(cmd))
     18 """ if(subprocess.check_call(cmd) == 0):
     19     print("Successfully updated stack metadata") """

/usr/lib/python3.6/subprocess.py in check_call(*popenargs, **kwargs)
    304     check_call(["ls", "-l"])
    305     """
--> 306     retcode = call(*popenargs, **kwargs)
    307     if retcode:
    308         cmd = kwargs.get("args")

/usr/lib/python3.6/subprocess.py in call(timeout, *popenargs, **kwargs)
    285     retcode = call(["ls", "-l"])
    286     """
--> 287     with Popen(*popenargs, **kwargs) as p:
    288         try:
    289             return p.wait(timeout=timeout)

/usr/lib/python3.6/subprocess.py in __init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, encoding, errors)
    727                                 c2pread, c2pwrite,
    728                                 errread, errwrite,
--> 729                                 restore_signals, start_new_session)
    730         except:
    731             # Cleanup if the child failed starting.

/usr/lib/python3.6/subprocess.py in _execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, start_new_session)
   1362                         if errno_num == errno.ENOENT:
   1363                             err_msg += ': ' + repr(err_filename)
-> 1364                     raise child_exception_type(errno_num, err_msg, err_filename)
   1365                 raise child_exception_type(err_msg)
   1366 

FileNotFoundError: [Errno 2] No such file or directory: 'exiftool -csv=./data/RedEdge3/stacks/log.csv -overwrite_original ./data/RedEdge3/stacks': 'exiftool -csv=./data/RedEdge3/stacks/log.csv -overwrite_original ./data/RedEdge3/stacks'