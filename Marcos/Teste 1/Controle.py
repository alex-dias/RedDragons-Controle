# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:06:36 2017

@author:     Marcos
"""

import math
from math import pi
import numpy as np
import time

def controle(RD, alvo, constX, constY):
    
    debug = True
    #debug = False
    AtingiuOAlvo = False
    
    angulo_r = RD[2]
    pos_x_r = RD[0] * constX
    pos_y_r = RD[1] * constY
    
    alvo[0] = alvo[0] * constX
    alvo[1] = alvo[1] * constY
    
    veloc_r = 5
    L_r = 7.5

    rodaR = 0
    rodaL = 0

    #informações do alvo
    pos_x_a = alvo[0]               
    pos_y_a = alvo[1]

    
    
    #informações do controle
    KP = 0.4
    KD = 0

    
    #calculo do angulo desejado
    delta_x = pos_x_a - pos_x_r
    delta_y = pos_y_a - pos_y_r    
    angulo_d = np.arctan2(delta_y,delta_x)
    
    #if delta_x < 0 and delta_y > 0:
    #    angulo_d = angulo_d + pi

    #if delta_x < 0 and delta_y < 0:
    #    angulo_d = angulo_d - pi
    
    # Erro do angulo
    angulo_e = angulo_d - angulo_r

    # trunca o erro do angulo entre-180 e 180
    angulo_e = np.mod(angulo_e,1.7*pi)
    if angulo_e > pi:
        angulo_e = angulo_e - 2*pi 

    #pid
    angulo_r = angulo_r + KP*angulo_e

    # distancia absoluta do robo para o alvo
    distRA = math.sqrt((pos_x_r - pos_x_a)**2 + (pos_y_r - pos_y_a)**2)
    
    # se distancia menor que X, o robo para
    if(distRA<=5):
        rodaL = 0
        rodaR = 0
        AtingiuOAlvo = True
    
    else:
        # Diminui a velocidade inversamente proporcional a distancia do alvo
        #if (distRA<=20):
            #veloc_r = veloc_r*(distRA/10)  
            
        #KD = 0 => KD * angulo_e = 0 com isso não esta sendo utilizado o controle derivativo, apenas o controle derivativo 
        VL = veloc_r - KP * angulo_e - KD * angulo_e
        VR = veloc_r + KP * angulo_e + KD * angulo_e

        maxV = max(VL, VR)

        #Realiza uma conversão caso a velocidade mais alta dentre as duas rodas for mais alta que a velocidade maxima
        if (maxV > veloc_r):
            constSat = veloc_r/maxV
            VL = VL * constSat
            VR = VR * constSat

        #Constante para alterar o intervalo de velocidade
        constVel = (300/5)

        #Trecho para converter o valor entre -5 e 5 na faixa desejada
        if(VL >= -5 and VL <= 5):
            rodaL = round(VL*constVel)
        else:
            rodaL = 0
        if(VR >= -5 and VR <= 5):
            rodaR = round(VR*constVel)
        else:
            rodaR = 0

        #Trecho sem sentido para a simulação mas necessário para o controle
        """
        if(rodaL < 0):
            rodaL = -rodaL
            sentidoL = 0
        else:
            sentidoL = 1

        if(rodaR < 0):
            rodaR = -rodaR
            sentidoR = 0
        else:
            sentidoR = 1
        """

    if debug:
        #print "constantes:"
        #print constX
        #print constY
        print ("Posicao X: %f" % pos_x_r)
        print ("Posicao Y: %f" % pos_y_r)
        print ("Posicao alvo X: %f" % alvo[0])
        print ("Posicao alvo Y: %f" % alvo[1])
        print('Distancia: %f' % distRA)
        print("rodal: %d" % rodaL)
        print("rodaR: %d" % rodaR)
        #print("sentidoL: %d" % sentidoL)
        #print("sentidoR: %d" % sentidoR)
        
    return rodaR, rodaL, AtingiuOAlvo