# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 19:53:02 2017

@author: geo
"""

import cv2
import numpy as np
import copy
import os.path
import filtro
import time


##############
# NO MAIN, ADQUIRIMOS O ORIGINAL 'SNAP' 
# NA CALIBRAÇÃO, TRABALHAMOS COM 'SNAPE', UMA CÓPIA DE 'SNAP' QUE PODEMOS ALTERAR 
#For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
##############

#==== [FUNÇÃO AUXILIAR, RETORNA NADA] =========================================
def nothing(x):     # Essa função é necessária para construir os trackbars
    pass


#==== [PERMITE VISUALIZAR IMAGENS NA INTERFACE GRÁFICA] =======================
def visualizacao(snap):    
    global snape
    snape = copy.deepcopy(snap)        #Calibração de Cores de amostra

#==== [SALVA POSICÃO COM CLIQUE DUPLO DO MOUSE] ===============================
def mouse_click(event,x,y,flags,param):     
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(snape,(x,y),3,(255,255,0),-1)
        mouseX,mouseY = x,y


#==== [ABRE A CAMERA E TIRA FOTO PARA TESTAR] =================================
def snapshot(video):
    cv2.namedWindow('Câmera')
    cv2.moveWindow('Câmera',200,200)
    cap = cv2.VideoCapture(video)
    frame_counter = 0
    
    while True:        
        
        ret, snap = cap.read()
        frame_counter += 1

        if frame_counter == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):   #Conta frames para recomeçar o vídeo quando acabar
            frame_counter = 0
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)  

        if ret == False:
            print ('Falha no Vídeo')
            print ('Carregando último Snapshot')
            break    
        
        if (cv2.waitKey(1) & 0xFF == ord('f')):
            cv2.imwrite('snap.png', snap)
            break
        
        cv2.imshow('Câmera', snap)
        
    cv2.destroyAllWindows()
    return snap

    

#==== [ADQUIRE PARÂMETROS DO CAMPO] ===========================================
def parametro(snap, flag_parametros):
    
    n=3     #Numero de parâmetros
    
    
    parametros = np.zeros([n,2],dtype=int)  #Inicializa vetor nulo pra receber parâmetros do campo
    
    if flag_parametros == True:
        
        cv2.namedWindow('Calibração de Parâmetros do Campo')
        cv2.moveWindow('Calibração de Parâmetros do Campo', 200, 200)
        cv2.setMouseCallback('Calibração de Parâmetros do Campo',mouse_click)
        

        for i in xrange(0,n):    
            if i==0:
                print('Selecione a borda SUPERIOR ESQUERDA do campo')
            if i==1:
                print('Selecione a borda SUPERIOR DIREITA do campo')
            if i==2:
                print('Selecione a borda INFERIOR ESQUERDA do campo e pressione ')
                
            while(1):
                
                cv2.imshow('Calibração de Parâmetros do Campo', snape)
                                
                k = cv2.waitKey(20) & 0xFF
                if (k == ord('f') or i==3):     #Aperte 'f' para fechar a janela                
                    if os.path.isfile("parametros.npy") == True:
                        parametros = np.load('parametros.npy')
                        cv2.destroyAllWindows()
                        flag_parametros = False
                        break
                    else:
                        print('É necessário selecionar os parâmetros do campo!')
                
                elif k == ord('s') and i<n:
                    parametros[i] = (mouseX,mouseY)
                    print(parametros[i])
                    break
        
                if i == 3:
                    break
            if flag_parametros == False:
                break
        cv2.destroyAllWindows()
    
    else:
        parametros = np.load('parametros.npy')
    
    origem = parametros[0]
    np.save('parametros',parametros)
    return parametros, origem


#==== [CORTA A IMAGEM] ========================================================
def crop(img,parametros,mostrar):
    imagem=img[parametros[0,1]:parametros[2,1], parametros[0,0]:parametros[1,0]]
    if mostrar == True:
        cv2.imshow('image',imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return imagem


#==== [ CALIBRAÇÃO ] =========================================================
def color(snap_amostra,n_amostras,ch,parametros,video,area_minima):
    
    a = n_amostras    
    pixel_pos = np.zeros([a,2], dtype=np.int16)             #Matriz com a posicao das amostras de pixel
    pixel_color = np.zeros([a,3], dtype=np.int16)           #Matriz com os valores BGR das amostras de pixel
    lower = np.zeros([a,ch], dtype=np.int16)                 #treshold inferior das amostras
    upper = np.zeros([a,ch], dtype=np.int16)                 #treshold superior das amostras
    calib = np.zeros([a,7], dtype=np.int16)                 #Matriz que guarda todos os dados de calibração individuais pra cada amostra
    mask1 = np.zeros([snap_amostra.shape[0],snap_amostra.shape[1]])
    img = np.zeros([snap_amostra.shape[0],snap_amostra.shape[1], ch])  
    frame_counter = 0
    
    
    cap = cv2.VideoCapture(video)
    
    visualizacao(snap_amostra)
    snap_hsv_amostra = cv2.cvtColor(snap_amostra,cv2.COLOR_BGR2HSV)    

    # Carrega calibração anterior como um preset para a calibração atual
    if os.path.isfile('calib.npy'):            
        cali = np.load('calib.npy')
        if len(cali) <= len(calib):
            z = len(cali)
        else:
            z = len(calib)
            
        for j in xrange (0,z):
            calib[j] = cali[j]
    
    
    # ------------------[ LOOP PRINCIPAL ]-------------------------------------
    for i in xrange (0,n_amostras):
        
        cv2.namedWindow('Selecione o ponto de amostragem de cor')
        cv2.moveWindow('Selecione o ponto de amostragem de cor', 200, 200)
        cv2.setMouseCallback('Selecione o ponto de amostragem de cor',mouse_click)
        
    # Seleciona amostra de cor -----------------------------------------------
        while(1):
            
            cv2.imshow('Selecione o ponto de amostragem de cor',snape)
            
            k = cv2.waitKey(20) & 0xFF
            if (k == ord('f')):
                cv2.destroyAllWindows()
                
                if os.path.isfile('pixel_color.npy'):
                    print('Carregando calibração anterior')
                    pixel_color[i] = calib[i,0:3]
                    break
                else:
                    print('Necessário escolher as amostras de cor!')
                    
    
            elif k == ord('s'):
                pixel_pos[i] = (mouseX,mouseY)
                (Hi,Si,Vi) = snap_hsv_amostra[pixel_pos[i,1],pixel_pos[i,0]]
                pixel_color[i] = [Hi,Si,Vi]
                
                print('Posição')
                print pixel_pos[i]
                print ('Cor')
                print pixel_color[i]
                
                cv2.destroyAllWindows()
                break
            
        cv2.destroyAllWindows()
        
    # Ajuste fino da amostra de cor -------------------------------------------
        
        cv2.namedWindow('Ajuste fino')
        cv2.moveWindow('Ajuste fino', 100, 100)
        cv2.namedWindow('Máscara')
        cv2.moveWindow('Máscara', 500, 100)
            
        
        cv2.createTrackbar('H', 'Ajuste fino', pixel_color[i,0],179, nothing)        
        cv2.createTrackbar('S', 'Ajuste fino', pixel_color[i,1],255, nothing)
        cv2.createTrackbar('V', 'Ajuste fino', pixel_color[i,2],255, nothing)
        cv2.createTrackbar('Treshold', 'Ajuste fino', calib[i,3] ,100, nothing)   
        cv2.createTrackbar('Força do Filtro', 'Ajuste fino', calib[i,5] ,50, nothing)
        cv2.createTrackbar('Tipo do Filtro', 'Ajuste fino', calib[i,4],3,nothing)
        cv2.createTrackbar('Estático', 'Ajuste fino', calib[i,6] ,1, nothing)
        cv2.createTrackbar('0 : OFF \n1 : ON', 'Ajuste fino',1,1,nothing)
        
        
        view = copy.deepcopy(snap_amostra)
        
        while(1):
            
            cv2.imshow('Máscara',view)
            
            
            if calib[i,6] == 1:         #Calibra mostrando video em tempo real
                ret, view = cap.read()
                view = crop(view,parametros,False)
                snap_hsv = cv2.cvtColor(view,cv2.COLOR_BGR2HSV)
                
                frame_counter += 1
                
                #Loop do video
                if frame_counter == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT): 
                    frame_counter = 0 
                    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
                
            else:
                    snap_hsv = snap_hsv_amostra[:]
                    view = snap_amostra[:]
            
            
            k = cv2.waitKey(20) & 0xFF
            if (k == ord('f')):     #Aperte 'f' para fechar a janela
                calib_old = np.load('calib.npy')
                calib[i] = calib_old[i]
                cv2.destroyAllWindows()
                break
            

            
            # Atualiza HSV em relação à posição dos trackbars em tempo real
            H = cv2.getTrackbarPos('H', 'Ajuste fino')
            S = cv2.getTrackbarPos('S', 'Ajuste fino')
            V = cv2.getTrackbarPos('V', 'Ajuste fino')
            th = cv2.getTrackbarPos('Treshold', 'Ajuste fino')
            fi = cv2.getTrackbarPos('Tipo do Filtro', 'Ajuste fino')
            ke = cv2.getTrackbarPos('Força do Filtro', 'Ajuste fino')
            est = cv2.getTrackbarPos('Estático', 'Ajuste fino')
            show = cv2.getTrackbarPos('0 : OFF \n1 : ON','Ajuste fino')
            


            img = snap_hsv[:,:,0:ch]
            inf = np.array([H-th, S-th, V-th]) 
            lower[i] = inf[0:ch]
            sup = np.array([H+th, S+th, V+th]) 
            upper[i] = sup[0:ch]
                
            if show == 1:
                
                
                mask1 = cv2.inRange(img, lower[i], upper[i])    
                
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
                    
                mask1 = filtro.morph(mask1,fi,ke)
                view = cv2.bitwise_and(view,view,mask=mask1)
                
                
            calib[i] = [H, S, V, th, fi, ke, est]

            if k == ord('s'):
                np.save('calib',calib)
                cv2.destroyAllWindows()
                break
           
    
    # Processamento -----------------------------------------------------------
            cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0]
            
            for c in cnts:
            	# Calcula centroides
                
                M = cv2.moments(c)
                
                if  M["m00"] >= area_minima and M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    # Desenha círculo branco no centroide da forma
                    cv2.circle(view, (cX, cY), 2, (255, 255, 255), -1)
            
    np.save('pixel_pos', pixel_pos)    
    np.save('pixel_color',pixel_color)
    np.save('lower', lower)
    np.save('upper', upper)
    
    print ('-----------------------------')   
    print('Amostras de cor:')
    print (pixel_color)
#    cv2.destroyAllWindows()
          
    
    return calib, upper, lower, mask1
    
    
#==== [ TRACKING ] =========================================================
def tracking(lower,upper,modelo, calib,ch, parametros,area_minima,cap,frame_counter,aquisicao):
    
    [x,y] = modelo.shape
    mask1 = np.zeros([x,y], dtype=np.uint8)    
    a = len(calib)
    quebra = False
    robot = np.zeros([a,3])     
    mask1 = np.zeros([x,y], dtype=np.uint8)
    
    ret,frame = cap.read()
    frame = crop(frame,parametros,False)
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    img= frame_hsv[:,:,0:ch]
    
    frame_counter += 1
        
    #Loop do video
    if aquisicao == -1 and frame_counter == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT): 
        frame_counter = 0 
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
                    
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
                                
        robot = orientacao(robot,centroids,a)         
        cv2.circle(frame, (int(robot[0,0]),int(robot[0,1])), 7, (0, 0, 255), -1)
        mask1 = cv2.bitwise_or(mask1,mask2)
                    
    frame = cv2.bitwise_and(frame,frame,mask=mask1)
    
    cv2.imshow("Tracking",frame)
    
    k = cv2.waitKey(20) & 0xFF
    if (k == ord('f')):
        quebra = True
    
    return quebra, frame_counter
    
    
def mascara(mask1,calib,img,lower,upper,modo):
    x,y,z = img.shape
    
    if modo == 1:
        for i in xrange (0, len(calib)):
            mask2 = mask1[:]
            mask1 = np.zeros([x,y], dtype=np.uint8)     
            mask1 = cv2.inRange(img,lower[i],upper[i])
            mask1 = filtro.morph(mask1,calib[i,4],calib[i,5])
            mask1 = cv2.bitwise_or(mask1,mask2)
    
    if modo == 2:
#        pass
        mask1 = img[0] > lower[1,0] #and img < upper[1,0]
                    #print 'YaY!'
    
        #cv2.imshow('testin',mask1)
    
    
    return mask1