#!/usr/bin/env python
# coding: utf-8

# Python program to compute and visualize the
# histogram of Blue channel of image

# importing libraries
import sys, time, os, datetime, glob
import cv2
import argparse
import numpy as np
from matplotlib import pyplot as plt

from platform import python_version

print(f"(Sys version) :|: {sys.version} :|:")
os.system("which python")
print(f"(Python version) :#: {python_version()} :#:")

# reading the input image
img = cv2.imread('mountain.png')
#img = cv2.imread('dark_tones.jpg')

img_blue = img[:,:,2]
img_green = img[:,:,1]
img_red = img[:,:,0]

# split the image into its BGR components
(B, G, R) = cv2.split(img)
# find the maximum pixel intensity values for each
# (x, y)-coordinate,, then set all pixel values less
# than M to zero
M = np.maximum(np.maximum(R, G), B)

print(B.min(),B.max())
print(G.min(),G.max())
print(R.min(),R.max())

print(M.min(),M.max())


R[R < M] = 0
G[G < M] = 0
B[B < M] = 0

# print(R)
# print(G)
# print(B)
# merge the channels back together and return the image
mergeimg=cv2.merge([B, G, R])

# print(max(img_blue))
# print(min(img_blue))
# print(max(img_green))
# print(min(img_green))
# print(max(img_red))
# print(min(img_red))

# plot the above computed histogram
plt.imshow(mergeimg)
plt.title('Image Histogram For Blue Channel GFG')
plt.show()

# computing the histogram of the blue channel of the image
hist = cv2.calcHist([img],[0],None,[256],[0,256])

print(hist.min(),hist.max())

# np.savetxt(time.strftime("%Y%m%d_%H%M%S")+"_Blue.csv", np.vstack((hist)).T, delimiter=', ')
# np.savetxt(time.strftime("%Y%m%d_%H%M%S")+"_Blue.csv", np.vstack((hist)), delimiter=', ')
np.savetxt("mountain_Blue.csv", np.vstack((hist)), delimiter=', ')

# plot the above computed histogram
plt.plot(hist, color='b')
plt.title('Image Histogram For Blue Channel GFG')
plt.show()

# reading the input image
img = cv2.imread('mountain.png')
#img = cv2.imread('dark_tones.jpg')

# computing the histogram of the green channel of the image
hist = cv2.calcHist([img],[1],None,[256],[0,256])

# plot the above computed histogram
plt.plot(hist, color='g')
plt.title('Image Histogram For Green Channel GFG')
plt.show()

# reading the input image
img = cv2.imread('mountain.png')
#img = cv2.imread('dark_tones.jpg')

# computing the histogram of the Red channel of the image
hist = cv2.calcHist([img],[2],None,[256],[0,256])

# plot the above computed histogram
plt.plot(hist, color='r')
plt.title('Image Histogram For Red Channel GFG')
plt.show()

# reading the input image
img = cv2.imread('mountain.png')
#img = cv2.imread('dark_tones.jpg')

# define colors to plot the histograms
colors = ('b','g','r')

# compute and plot the image histograms
for i,color in enumerate(colors):
	hist = cv2.calcHist([img],[i],None,[256],[0,256]) # bit depth to 8-bit "BIT DEPTH"
	plt.plot(hist,color = color) # bit depth to 8-bit "BIT DEPTH"
plt.title('Image Histogram GFG')
plt.show()

print(type(img))
print(img.shape)
print(type(img.shape))

h, w, c = img.shape
print('width:  ', w)
print('height: ', h)
print('channel:', c)

h, w, _ = img.shape
print('width: ', w)
print('height:', h)

print('width: ', img.shape[1])
print('height:', img.shape[0])

print(img.shape[1::-1])

print(len(hist))
print(len(color))

image = cv2.imread('dark_tones.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
plt.plot(histogram, color='k')
plt.show()

image = cv2.imread('dark_tones.jpg')

for i, col in enumerate(['b', 'g', 'r']):
    hist = cv2.calcHist([image], [i], None, [256], [0, 256])
    plt.plot(hist, color = col)
    plt.xlim([0, 256])
    
plt.show()

w=cv2.imread('mountain.png',1)
cv2.imshow('image',w)
b,g,r = cv2.split(w)
height = np.size(w, 0)
width = np.size(w, 1)
bw = np.zeros((height,width))
  
# for i in range(1,height):
#     for j in range(1,width):
#         if(b[i,j]<g[i,j] and r[i,j]<g[i,j] and g[i,j]>125):
#             bw[i,j]=1
# cv2.imshow('Black and White image',bw)
# kernel = np.ones((5,5),np.uint8)
# bw= cv2.erode(bw,kernel,iterations = 4)
# cv2.imshow('Eroded image',bw)
# bw = cv2.dilate(bw,kernel,iterations = 3)
# cv2.imshow('Final Image',bw)
# cv2.waitKey(0)
# cv2.destroyAllWindows()