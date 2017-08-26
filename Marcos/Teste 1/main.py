#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2006-2017 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
#
# No script do v-rep, adicione o seguinte código
#
# simExtRemoteApiStart(19999)
#
# Então, inicie a simulação e execute esse programa.

#Importando a biblioteca time
import time
from Controle import controle
import numpy as np

#Importando a biblioteca do V-rep e em caso de excessão, imprime uma mensagem de erro
try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" Não pode ser carregado. Isso pode ter sido causado')
    print ('pelo "vrep.py" ou a biblioteca remoteApi não pode ser encontrada.')
    print ('Certifique-se que estes arquivos estejam no mesmo diretório,')
    print ('ou realize os ajustes necessários no arquivo "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
    

#Variáveis globais
alvo = np.zeros([2])
RD = np.zeros([3])

alvo[0] = 70
alvo[1] = 70

print ('Programa iniciado!')
print ('V-rep importado com sucesso!')

#Fecha todas as conexões abertas
vrep.simxFinish(-1)
#Conecta com o servidor do v-rep
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

#Verifica por clientes ativos
if clientID!=-1:
    #Caso exista um cliente ativo, mostra a mensagem de execução bem sucedida
    print ('Conectadoo com sucesso ao API do servidor remoto')

    #Fazendo a ligação com o robo e caso não seja bem sucedida, apresenta o código do erro
    errorCodeRobo, robot = vrep.simxGetObjectHandle(clientID, 'ePuck', vrep.simx_opmode_blocking)

    if errorCodeRobo == 0:
        print ('Comunicaçao com o robo bem sucedida')
    else:
        print ('Falha ao se comunicar com o robo')
        print ('Código de erro: {0}' .format(errorCoderight))

    #Fazendo a ligação com o motor esquerdo e caso não seja bem sucedida, apresenta o código do erro
    errorCodeleft, left_motor_handle = vrep.simxGetObjectHandle(clientID, 'ePuck_leftJoint', vrep.simx_opmode_blocking)
    
    if errorCodeleft == 0:
        print ('Comunicaçao com o motor esquerdo bem sucedida')
    else:
        print ('Falha ao se comunicar com o motor esquerdo')
        print ('Código de erro: {0}' .format(errorCodeleft)) 

    #Fazendo a ligação com o motor direito e caso não seja bem sucedida, apresenta o código do erro
    errorCoderight, right_motor_handle = vrep.simxGetObjectHandle(clientID, 'ePuck_rightJoint', vrep.simx_opmode_blocking)
    
    if errorCoderight == 0:
        print ('Comunicaçao com o motor direito bem sucedida')
    else:
        print ('Falha ao se comunicar com o motor direito')
        print ('Código de erro: {0}' .format(errorCoderight))
        
        
    vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, 0, vrep.simx_opmode_streaming)
    vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, 0, vrep.simx_opmode_streaming)
    
    time.sleep(5)

    #Configurando a chamada para o ângulo
    errorCodeAngles, angles = vrep.simxGetObjectOrientation(clientID, robot, -1, vrep.simx_opmode_streaming)
    
    #Configurando a chamada para a posição
    errorCodePos, posicion = vrep.simxGetObjectPosition(clientID, robot, -1, vrep.simx_opmode_streaming)
    
    time.sleep(0.02)
    
    #Variável controladora do loop
    AtingiuOAlvo = False
    
    while not(AtingiuOAlvo):
        #Recebendo a posição dos robôs (o delay é necessário para receber a resposta do v-rep)
        errorCodePos, posicion = vrep.simxGetObjectPosition(clientID, robot, -1, vrep.simx_opmode_buffer)
        
        #Recebendo os ângulos dos robôs (o delay é necessário para receber a resposta do v-rep)
        errorCodeAngles, angles = vrep.simxGetObjectOrientation(clientID, robot, -1, vrep.simx_opmode_buffer)
        
        
        RD[0] = int(posicion[0]*100)
        RD[1] = int(posicion[1]*100)
        RD[2] = (angles[1])
        
        alvo[0] = 70
        alvo[1] = 70
        
        velDir, velEsq, AtingiuOAlvo = controle(RD, alvo, 1, 1)
        
        time.sleep(0.5)
        
        #Configurando a velocidade dos motores
        vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, velEsq/100, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, velDir/100, vrep.simx_opmode_streaming)
        
        if velDir == 0 and velEsq == 0:
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, 0, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, 0, vrep.simx_opmode_streaming)
            
            time.sleep(0.2)
            
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, 0, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, 0, vrep.simx_opmode_streaming)
else:
    print ('Falha ao conectar com a API do servidor remoto')
    
print ('Program ended')



