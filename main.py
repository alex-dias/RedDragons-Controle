# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 19:42:28 2017

@author: geo
"""

#importaçõe da visao
import cv2
import numpy as np
import calibracao
import tracking
import time

#importações do controle
import serial, auxiliar
from PrincipalFuncao import  *
from robo import *

#=====[Definições do controle]=========
robo1 = Robo()
temXbee = True
bola = np.zeros([1,2])
RD = np.zeros([1,3])

if(temXbee):
    porta = "/dev/ttyUSB0"			#Xbee
    velocidade = 57600
    
    ser = serial.Serial(porta, velocidade)

    
# =====[ VARIÁVEIS DE AJUSTE]=====
aquisicao = 0      #Entrada de Vídeo: 0=Camera interna, 1=Camera USB, -1=Template
a = 3              #Numero de amostras
thi = 55        #Treshold inicial  
ch = 2     #Numero de canais de vídeo a serem considerados (HSV)
filtro_i = 5
calibrar = False


parametros = True
#par = False


area_minima = 10
    

# =====[ PRÉ PROCESSAMENTO]=====
if aquisicao == -1:
    gravacao = "visao.mp4"
else:
    gravacao = aquisicao

snap = calibracao.snapshot(gravacao)
calibracao.visualizacao(snap)
parametros, origem = calibracao.parametro(snap,parametros)
print('Parâmetros:')
print parametros

calibracao.visualizacao(snap)
snap = calibracao.crop(snap,parametros,False)

calib, upper, lower, mask1 = calibracao.color(snap,a,ch,parametros,gravacao,area_minima)


# =====[ TRACKING ]=====
cap = cv2.VideoCapture(gravacao)
frame_counter = 0    
cv2.namedWindow("Tracking")
cv2.moveWindow("Tracking",200,200)  

# =====[ LOOP PRINCIPAL ]=====
while (1):
    #start = time.time()         # Inicia a contagem do tempo (teste de desempenho)
    
    # Captura frames e recorta a imagem
    ret,frame = cap.read()
    frame = calibracao.crop(frame,parametros,False)    
    frame_counter += 1
        
    # Permite rodar arquivos de vídeo em loop caso não use a câmera.
    if aquisicao == -1 and frame_counter == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT): 
        frame_counter = 0 
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
     
    # Tracking dos robôs e da bola
    quebra, robot = tracking.tracking(lower,upper, frame, calib,ch, parametros,area_minima,cap,aquisicao)  
    
    # Condição de quebra do loop (finaliza o software)
    if quebra == True:
        break
    
    # =====[ CONTROLE ]===========================================================

    campo_maxY = parametros[2, 1]

    campo_maxX = parametros[1, 0]
	
    origem = (parametros[0, 0],parametros[0, 1])
    
    bola = [robot[0,0], robot[0,1]]
    
    RD[0,0] = robot[1,1]
    RD[0,1] = robot[1,0]
    RD[0,2] = robot[1,2]
    
    funcaoPrincipal(robo1, RD, campo_maxX, campo_maxY, origem, bola, ser)
#==============================================================================
    
    #end = time.time()           # Termina a contagem do tempo (teste de desempenho)
    #print end-start

    