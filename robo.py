# -*- coding: utf-8 -*-
from auxiliar import *

class Robo:

	######################### CONSTRUTOR
	def __init__(self):
		self.funcao = 'd'           #Função do jogar em campo; d == default; g == Goleiro; a == Atacante; z == Zagueiro 

		self.posicaoX = 0.0;
		self.posicaoY = 0.0;

		self.alvoX = 0.0;
		self.alvoY = 0.0;

		self.theta = 0;
		self.dTheta = 0;

		self.thetaDesejado = 0;
		self.dThetaDesejado = 0;

		self.thetaErro = 0;
		self.dThetaErro = 0;

		self.velMax = 5.0;
		self.consProporcional = 0.50;
		self.consDerivativa = 0;
		self.consVelocidade = 1;
		self.consRotacao = 1;
		self.epsilon = 10;

		self.distanciaVelocidadeMax = 200;
		self.distanciaVelocidadeZero = self.epsilon;

		self.tamanhoRobo = 75;
		self.tempo = 0.001;
		self.velocidade = self.velMax;

	######################### SETS

	def setfuncao(self, funcao):
		self.funcao = funcao
	
	def setPosicao(self, x, y):
		self.posicaoX = x;
		self.posicaoY = y;
	
	def setAlvo(self, x, y):
		self.alvoX = x;
		self.alvoY = y;

	def setVelocidade(self, v):
		self.velocidade = max(min(v, self.velMax), -self.velMax);

	def setDistanciaVelocidadeMax(self, d):
		self.distanciaVelocidadeMax = d;

	def setDistanciaVelocidadeZero(self, d):
		self.distanciaVelocidadeZero = d;
		
	def setTheta1(self, t):
		self.theta = t
		self.calculaErroAngulo()

	def setTheta(self, t, dt):
		self.theta = t
		self.dTheta = dt
		self.calculaErroAngulo()

	def setThetaDesejado(self, t, dt):
		self.thetaDesejado = t
		self.dThetaDesejado = dt
		self.calculaErroAngulo()

	def setConsProporcional(self, c):
		self.consProporcional = c;

	def setConsDerivativa(self, c):
		self.consDerivativa = c;

	def setConsVelocidade(self, c):
		self.consVelocidade = c;

	def setEpsilon(self, e):
		self.epsilon = e;

	def setVelMax(self, v):
		self.velMax = v;

	######################### GETS

	def getfuncao(self):
		return self.funcao

	def getPosicaoX(self):
		return self.posicaoX

	def getPosicaoY(self):
		return self.posicaoY

	def getPosicao(self):
		return self.posicaoX, self.posicaoY;

	def getAlvo(self):
		return self.alvoX, self.alvoY;

	def getVelocidade(self):
		return self.velocidade;

	def getDistanciaVelocidadeMax(self):
		return self.distanciaVelocidadeMax;

	def getDistanciaVelocidadeZero(self):
		return self.distanciaVelocidadeZero;

	def getTheta(self):
		return self.theta, self.dTheta;

	def getThetaDesejado(self):
		return self.thetaDesesjado, self.dThetaDesejado;

	def getConsProporcional(self):
		return self.consProporcional;

	def getConsDerivativa(self):
		return self.consDerivativa;

	def getConsVelocidade(self):
		return self.consVelocidade;

	def getEpsilon(self):
		return self.epsilon;

	def getVelMax(self):
		return self.velMax;

	######################### MÉTODOS

	def distanciaParaAlvo(self):
		return sqrt((self.alvoX - self.posicaoX) ** 2 + (self.alvoY - self.posicaoY) ** 2)

	def distanciaParaPonto(self, x, y):
		return sqrt((x - self.posicaoX) ** 2 + (y - self.posicaoY) ** 2)

	def atingiuAlvo(self):
		return (self.distanciaParaAlvo() < self.epsilon)

	def atingiuAlvoX(self):
		return (abs(self.alvoX - self.posicaoX) < self.epsilon)

	def atingiuAlvoY(self):
		return (abs(self.alvoY - self.posicaoY) < self.epsilon)

	def atingiuAlvoBola(self):
		return ((abs(self.alvoX - self.posicaoX) < self.epsilon + 0.045) and (abs(self.alvoY - self.posicaoY) < self.epsilon + 0.035)) 
	
	def atingiuAngulo(self):
		return (abs(self.thetaErro) < self.epsilon);

	def posicaoXEmIntervalo(self, minimo, maximo):
		return (self.posicaoX >= minimo - self.epsilon and self.posicaoX <= maximo - self.epsilon)

	def posicaoYEmIntervalo(self, minimo, maximo):
		return (self.posicaoY >= minimo - self.epsilon and self.posicaoY <= maximo - self.epsilon)

	def calculaVelocidade(self):
		distAlvo = self.distanciaParaAlvo()
		if(distAlvo >= self.distanciaVelocidadeMax):
			velocidade = self.velMax
		elif(distAlvo > self.distanciaVelocidadeZero):
			velocidade = self.velMax * distAlvo * self.consVelocidade
		elif(self.atingiuAngulo()):
			velocidade = 0
		else:
			velocidade = self.thetaErro * self.velMax * self.consRotacao
		return velocidade

	def calculaErroAngulo(self):
		self.thetaErro = normalizeAngle(self.thetaDesejado - self.theta, -1.8*pi);
		self.dThetaErro = self.dThetaDesejado - self.dTheta;

	def moverEmX(self):
		tempY = self.alvoY;
		self.alvoY = self.posicaoY;
		self.irParaAlvo(False);
		self.alvoY = tempY;

	def moverEmY(self):
		tempX = self.alvoX;
		self.alvoX = self.posicaoX;
		self.irParaAlvo(False);
		self.alvoX = tempX;

	def irParaAlvo(self, mudarAngulo = True):

		if(mudarAngulo):
			self.thetaDesejado = atan2(self.alvoY - self.posicaoY, self.alvoX - self.posicaoX);
			self.calculaErroAngulo();
		
		print('velocidade {0}' .format(self.velocidade))
		
		VL, VR = controlPDRobot(self.velocidade, self.thetaErro, self.dThetaErro, self.consProporcional, self.consDerivativa, self.tamanhoRobo);
		
		comando = self.setMotor( VR, VL)
		
		velMedia = (VR + VL) / 2; 
		omega = (VR - VL) / self.tamanhoRobo;
		self.posicaoX, self.posicaoY, self.theta = robotSim(velMedia, omega, self.theta, self.posicaoX, self.posicaoY, self.tempo);

		return comando

	def debug(self):
		print("R:{8} X: {0}, Y: {1}, AX: {2}, AY: {3}, T: {4}, TD: {5}, TE: {6}, V: {7}".format(self.posicaoX, self.posicaoY, self.alvoX, self.alvoY, self.theta, self.thetaDesejado, self.thetaErro, self.velocidade, self.funcao));
		#raw_input()
	
	def setMotor(self, velocidadeR, velocidadeL):
		
		#print(velocidadeL)
		#print(velocidadeR)

		constVel = (5/1023)
		'''
		if(velocidadeL >= -5 and velocidadeL <= 5):
			rodaL = round(velocidadeL/constVel)
		else:
			rodaL = 0
		if(velocidadeR >= -5 and velocidadeR <= 5):
			rodaR = round(velocidadeR/constVel)
		else:
			rodaR = 0
		'''
		rodaL = round(1023 * (1 - ((abs (velocidadeL))/1023)))
		rodaR = round(1023 * (1 - ((abs (velocidadeR))/1023)))
		
		#print(rodaL)
		#print(rodaR)
		
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
		
		
		comando = "%d,%.4d,%d,%.4d" % (sentidoL, rodaL, sentidoR, rodaR)
		
		return comando

