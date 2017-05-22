# -*- coding: utf-8 -*-
"""
Created on Wed May  3 18:55:18 2017

@author: geo
"""

import cv2
import numpy as np
import time

def nothing(x):
    pass


img = cv2.imread('template.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(5,5))

cv2.namedWindow('Circulos usando Hough')
#cv2.createTrackbar('H', 'Ajuste fino', pixel_color[i,0],179, nothing)  

cv2.createTrackbar('dp', 'Circulos usando Hough', 16, 1000, nothing)
cv2.createTrackbar('minDist','Circulos usando Hough', 57, 1000, nothing)
cv2.createTrackbar('param1','Circulos usando Hough', 1, 1000, nothing)
cv2.createTrackbar('param2','Circulos usando Hough', 1, 1000, nothing)
cv2.createTrackbar('minRadius','Circulos usando Hough', 1, 1000, nothing)
cv2.createTrackbar('maxRadius','Circulos usando Hough', 1, 1000, nothing)

while(1):
    start = time.time()
    output = img.copy()
    #cv2.HoughCircles(image, method, dp, minDist)
    
    dp = cv2.getTrackbarPos('dp', 'Circulos usando Hough')    
    minDist = cv2.getTrackbarPos('minDist', 'Circulos usando Hough')
    param1 = cv2.getTrackbarPos('param1', 'Circulos usando Hough')
    param2 = cv2.getTrackbarPos('param2', 'Circulos usando Hough')
    minRadius = cv2.getTrackbarPos('minRadius', 'Circulos usando Hough')
    maxRadius = cv2.getTrackbarPos('maxRadius', 'Circulos usando Hough')
    
    
    if minDist == 0:
        minDist = 1
    if dp == 0:
        dp =1;
    if minDist == 0:
        minDist = 1
    if param1 == 0:
        param = 1
    if param2 == 0:
        param2 = 1
    if minRadius == 0:
        minRadius = 1
    if maxRadius == 0:
        maxRadius = 1
    
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT , dp, minDist, param1 ,param2 ,minRadius, maxRadius)
    #circles = None
    
    if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
     # loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)



    cv2.imshow('Circulos usando Hough',output)
    

    k = cv2.waitKey(20) & 0xFF
    if (k == ord('f')):     #Aperte 'f' para fechar a janela
        cv2.destroyAllWindows()
        break
    
    end = time.time()
    print end-start