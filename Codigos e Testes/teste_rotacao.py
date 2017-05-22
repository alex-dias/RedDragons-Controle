# -*- coding: utf-8 -*-
"""
Created on Mon May  1 22:32:11 2017

@author: geo
"""

import cv2
import numpy as np
import time

image = cv2.imread('snap.png')

def callback(x):
    pass

default1 = 0
max_val1 = 360
default2 = 100
max_val2 = 200
n=float(100.0)

cv2.namedWindow('Rotação')
cv2.createTrackbar('Correção do Ângulo', 'Rotação', default1, max_val1, callback)
cv2.createTrackbar('Escala', 'Rotação', default2, max_val2, callback)

while(1):
    start = time.time()
    theta = cv2.getTrackbarPos('Correção do Ângulo','Rotação')
    scale = np.float(cv2.getTrackbarPos('Escala','Rotação'))
    scale = scale/n
    H = cv2.getTrackbarPos('H', 'Ajuste fino')
    
    # grab the dimensions of the image and calculate the center
    # of the image
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
     
    # rotate the image by 180 degrees
    M = cv2.getRotationMatrix2D(center, theta, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    cv2.imshow("Rotação", rotated)
    
    k = cv2.waitKey(20) & 0xFF
    if (k == ord('f')):
        cv2.destroyAllWindows()
        break
    
    end = time.time()
    print end - start
    
    