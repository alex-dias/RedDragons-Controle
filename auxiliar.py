# -*- coding: utf-8 -*-

# Parte deste código foi criada com seus direitos restringidos ao uso mediante a inserção do nome do autor e fonte:
# Autor: Fernando Krein Pinheiro
# Data: 07/09/2011
# Linguagem: Python
# Fonte: https://ferpinheiro.wordpress.com/2011/09/07/usando-python-para-comunicar-com-a-porta-serial/

# ========= IMPORTANTE ===========
# O codigo esta livre para usar, citar e compartilhar desde que mantida sua fonte e seu autor.
# Obrigado.
import serial

from time import *
from math import *

epsilon = 0.00000000000001
epsilon2 = 0.01

def normalizeAngle(r, low):
	angle = r - 2 * pi * floor((r - low) / (2 * pi))
	return angle

def controlPDRobot(v, thetae, dthetae, KP, KD, L):
	KPl = L / 2 * KP;
	KDl = L / 2 * KD;
	VL = v - KPl * thetae - KDl * dthetae
	VR = v + KPl * thetae + KDl * dthetae
	 
	maxV = max(VL, VR)
	
	if (maxV > v):
		constSat = abs(v/maxV)
		
		VL = VL * constSat
		VR = VR * constSat
	
	return VL, VR

def robotSim(v, omega, thetaP, xP, yP, T):
	cosT = cos(thetaP)
	sinT = sin(thetaP)

	if(abs(cosT) < epsilon):
		cosT = 0
	if(abs(sinT) < epsilon):
		sinT = 0

	dx = v * cosT
	dy = v * sinT
	dtheta = omega
	x = dx * T + xP
	y = dy * T + yP
	theta = dtheta * T + thetaP
	return x, y, theta
	
def maisProximo(roboA, roboB, roboC, x, y):
	distanciaA = roboA.distanciaParaPonto(x, y)
	distanciaB = roboB.distanciaParaPonto(x, y)
	distanciaC = roboC.distanciaParaPonto(x, y)

	if((distanciaA <= distanciaB) and (distanciaA <= distanciaC)):
		return roboA
	elif((distanciaB <= distanciaA) and (distanciaB <= distanciaC)):
		return roboB
	elif((distanciaC <= distanciaB) and (distanciaC <= distanciaA)):
		return roboC

def serialEscreverPorta(ser, comando):
	if (ser.isOpen()):
		try:
			ser.flushInput() #flush input buffer, discarding all its contents
			ser.flushOutput()#flush output buffer, aborting current output
	
			ser.write(comando)

		except Exception, e:
			print "ERRO: " + str(e)
