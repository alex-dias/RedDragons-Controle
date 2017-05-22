# -*- coding: utf-8 -*-
"""
Created on Wed May 10 00:03:29 2017

@author: geo
"""

import numpy as np

def orientacao(robot, centroids,a):
    if a > 2 :
        for j in xrange (0,3):
            for k in xrange (2,a):

                dx = centroids[1,j,0]-centroids[k,0,0]
                dy = centroids[1,j,1]-centroids[k,0,1]
                dist = int((dx**2 + dy**2)**0.5)

                if dist != 0 and dist<30:
                    robot[0,0:2] = (centroids[1,j,0]+centroids[k,0,0])/2, (centroids[1,j,1]+centroids[k,0,1])/2
                    robot[0,2] = np.arctan2(dy,dx)
                    #print 'Robot:',' \n', robot
                    #print "\n" * 28
            
    return robot