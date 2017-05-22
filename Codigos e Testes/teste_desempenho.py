# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 21:39:16 2017

@author: geo
"""

import cv2
import numpy as np
import timeit
import time

frame = cv2.imread('snap.png')
print frame.shape
a = frame[:,:,0:2]
print a.shape

while(1):
    start = time.time()
    snap_hsv_amostra = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    end = time.time()

    print end-start
