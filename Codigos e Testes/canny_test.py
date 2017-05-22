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
#gray = cv2.blur(gray,(5,5))



## =================[ Criação das Trackbar] =================================
cv2.namedWindow('Canny')

cv2.createTrackbar('dp', 'Canny', 16, 1000, nothing)
cv2.createTrackbar('minDist','Canny', 57, 1000, nothing)
cv2.createTrackbar('param1','Canny', 1, 1000, nothing)
cv2.createTrackbar('param2','Canny', 1, 1000, nothing)
cv2.createTrackbar('minRadius','Canny', 1, 1000, nothing)
cv2.createTrackbar('maxRadius','Canny', 1, 1000, nothing)

while(1):
    start = time.time()
    #cv2.HoughCircles(image, method, dp, minDist)
    
    dp = cv2.getTrackbarPos('dp', 'Canny')    
    minDist = cv2.getTrackbarPos('minDist', 'Canny')
    param1 = cv2.getTrackbarPos('param1', 'Canny')
    param2 = cv2.getTrackbarPos('param2', 'Canny')
    minRadius = cv2.getTrackbarPos('minRadius', 'Canny')
    maxRadius = cv2.getTrackbarPos('maxRadius', 'Canny')
    
    
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
    



    view  = gray
    cv2.imshow('Canny',view)
    

    k = cv2.waitKey(20) & 0xFF
    if (k == ord('f')):     #Aperte 'f' para fechar a janela
        cv2.destroyAllWindows()
        break
    
    end = time.time()
    print end-start