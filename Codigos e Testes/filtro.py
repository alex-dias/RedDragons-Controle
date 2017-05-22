# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 21:00:10 2016

@author: GEO
"""

import cv2
import numpy as np

def morph(img,filtro,ke):
    
    if ke == 0:
        ke = 1    
        
    kernel = np.ones((ke,ke),np.float32)/(ke*ke)
    
    if filtro == 0:
        res = img
        
    if filtro == 1:
        res = cv2.erode(img,kernel)          # Faz erosão de cada mascara
    if filtro == 2:
        res = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    if filtro == 3:
        res = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        
    return res

    