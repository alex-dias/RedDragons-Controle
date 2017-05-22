# -*- coding: utf-8 -*-
"""
Created on Tue May  9 23:56:25 2017

@author: geo
"""
import cv2
import numpy as np
import filtro
import time
import orientacao
#==== [ TRACKING ] =========================================================
def tracking(lower,upper,frame, calib,ch, parametros,area_minima,cap,aquisicao):
    
    [x,y,_] = frame.shape
    mask1 = np.zeros([x,y], dtype=np.uint8)    
    a = len(calib)
    quebra = False
    robot = np.zeros([a,3])     
    mask1 = np.zeros([x,y], dtype=np.uint8)
    

    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    img= frame_hsv[:,:,0:ch]
                    
    centroids = np.zeros([a,10,2], dtype = np.int32)
    
    for i in xrange (0, len(calib)):
        
        start1 = time.time()
        mask2 = mask1.copy()
        mask1 = cv2.inRange(img,lower[i],upper[i])
        
        ####### CORREÇÃO DA SEGMENTAÇÃO DE VERMELHO  #################
        
        if lower[i,0]<0:
            lower_aux = np.array([lower[i,0]+179, lower[i,1:2]])
            upper_aux = np.array([179,upper[i,1:2]])
            mask1_aux = cv2.inRange(img, lower_aux, upper_aux)
            mask1 = cv2.bitwise_or(mask1,mask1_aux)
            
        if upper[i,0]>179:
            lower_aux = np.array([0, lower[i,1:2]])
            upper_aux = np.array([upper[i,0]-179,upper[i,1:2]])
            mask1_aux = cv2.inRange(img, lower_aux, upper_aux)
            mask1 = cv2.bitwise_or(mask1,mask1_aux)
            
        ###############################################################
        
        mask1 = filtro.morph(mask1,calib[i,4],calib[i,5])
        end1  = time.time()
        print end1 - start1
        
    ## Processamento
        cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]        
        cont = -1            
         
        for c in cnts:            
            M = cv2.moments(c)
            
            if  M["m00"] >= area_minima and M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.circle(frame, (cX, cY), 2, (255, 255, 255), -1)                
                cont += 1
                centroids[i,cont]=(cX,cY)
                                
        robot = orientacao.orientacao(robot,centroids,a)         
        cv2.circle(frame, (int(robot[0,0]),int(robot[0,1])), 7, (0, 0, 255), -1)
        mask1 = cv2.bitwise_or(mask1,mask2)
                    
    frame = cv2.bitwise_and(frame,frame,mask=mask1)
    
    cv2.imshow("Tracking",frame)
    
    k = cv2.waitKey(20) & 0xFF
    if (k == ord('f')):
        quebra = True
    
    return quebra, robot