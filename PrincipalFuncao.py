# -*- coding: utf-8 -*-
#! /usr/bin/env python
from auxiliar import *
from robo import Robo
from math import pi
import serial, time, cv2


def funcaoPrincipal(robo1, RD, CampoX, CampoY, origem, bola, ser):

	teste = False
	temXbee = True
	debug = True
	
	H = 130
	L = 150
	
	robo1Y = (130*RD[0,0])/(CampoX-origem[0])
	robo1X = (150*RD[0,1])/(CampoY-origem[1])
	theta1 = RD[0,2]
	
	bolaY = (130*bola[0])/(CampoX-origem[0])
	bolaX = (150*bola[1])/(CampoY-origem[1])		
	
	robo1.setPosicao(robo1X, robo1Y)
	robo1.setTheta1(theta1)
	
	limInferiorGol = L * 0.362
	golIntermediario = L * 0.5
	limSuperiorGol = L * 0.638

	golNosso = 10
	golAdversario = 400
	
	limInferiorCampo = 0.0
	limSuperiorCampo = L
	
	robo1.setAlvo(golNosso, limInferiorGol)

	if(not robo1.atingiuAlvoX()):
		velocidaderobo1 = robo1.calculaVelocidade()
		robo1.setVelocidade(velocidaderobo1)
		comandorobo1 = robo1.irParaAlvo()
		if(debug):
			robo1.debug()
			print "Entrou no robo1 nao atingiu o alvo" 
	else:	
		robo1.setThetaDesejado(pi / 2, 0)
		if(debug):
			robo1.debug()
			print "Robo atingiu o alvo"

		if(not robo1.atingiuAngulo()):
			robo1.setConsProporcional(100)
			if(debug):
				robo1.debug()
				print "robo atingiu o alvo mas não o angulo"
			robo1.setAlvo(golNosso, limSuperiorGol)
			velocidaderobo1 = robo1.calculaVelocidade()
			robo1.setVelocidade(velocidaderobo1)
			comandorobo1 = robo1.irParaAlvo()
			robo1.setConsProporcional(50)

		else:		
			if(robo1.posicaoYEmIntervalo(limInferiorGol, limSuperiorGol)):
				x, y = robo1.getPosicao()
				alvoY = max(limInferiorGol, min(limSuperiorGol, bolaY))
				robo1.setAlvo(golNosso, alvoY)
				velocidaderobo1 = robo1.calculaVelocidade()
				if(y > alvoY):
					velocidaderobo1 *= -1
				robo1.setVelocidade(velocidaderobo1)
				robo1.moverEmY()
				comandorobo1 = robo1.irParaAlvo()
				if(debug):
					robo1.debug()
					print "robo atingiu o alvo e esta no intervalo y"
			else:
				x, y = robo1.getPosicao()
				if(robo1.distanciaParaPonto(golNosso, limInferiorGol) < robo1.distanciaParaPonto(golNosso, limSuperiorGol)):
					alvoY = limInferiorGol
				else:
					alvoY = limSuperiorGol
				robo1.setAlvo(golNosso, alvoY)
				velocidaderobo1 = robo1.getVelMax()
				if(y > alvoY):
					velocidaderobo1 *= -1
				robo1.setVelocidade(velocidaderobo1)
				robo1.moverEmY()
				comandorobo1 = robo1.irParaAlvo()
				if(debug):
					robo1.debug()	
					print "robo atingiu o alvo e não esta no intervalo y"

	if(temXbee):
		print('&' + comandorobo1 + '#')	
		serialEscreverPorta(ser, '&' + comandorobo1 + '#')
		serialEscreverPorta(ser, '$' + comandorobo1 + '#')
		serialEscreverPorta(ser, '@' + comandorobo1 + '#')

	if(teste):	
		RD[0] = [robo1X, robo1Y, theta1]
		print "X: " 
		print robo1X 
		print "Y: " 
		print robo1Y
	
		return RD
