#!/usr/bin/env python
# coding: utf-8

# Python program to compute and visualize the
# histogram of Blue channel of image
# %matplotlib inline

# importing libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt

# reading the input image
#img = cv2.imread('mountain.png')
img = cv2.imread('dark_tones.jpg')

# computing the histogram of the blue channel of the image
hist = cv2.calcHist([img],[0],None,[256],[0,256])

# plot the above computed histogram
plt.plot(hist, color='b')
plt.title('Image Histogram For Blue Channel GFG')
plt.show()