import pygame
from Proyectil import *
from random import randint,uniform,choice
class Invasor():
	def __init__(self,posx,posy,distancia, imagenes_invasores,disparos_invasor,tipo,resolución):
		self.resolución = resolución
		self.listaimagenes = imagenes_invasores[tipo]
		self.sonido_disparo = pygame.mixer.Sound('./Sonidos/DIVE.ogg')
		self.imagen_disparo = disparos_invasor[tipo]

		if tipo == 0:
			self.rangoDisparo = 1 #Determina la probabilidad de disparo
		if tipo == 1:
			self.rangoDisparo = 2
		elif tipo == 2:
			self.rangoDisparo = 3

		self.posImagen = 0	
		self.imagenInvasor = self.listaimagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()
		self.listadisparo = []
		self.velocidad = 1
		self.rect.top = posy
		self.rect.left = posx
		
		self.tiempoCambio = 3
		self.conquista = False
		self.derecha = True
		self.contador = 0
		self.Maxdescenso = self.rect.top + 40
		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx
		self.seLanza = False

	def dibujar(self,superficie):
		self.imagenInvasor = self.listaimagenes[self.posImagen]

		superficie.blit(self.imagenInvasor,self.rect)

	def comportamiento(self,tiempo,tiempo2,seLanza,índiceLance,jugador,id_objetivo,listaExplosiones):
		#algoritmo de comportamiento
		self.seLanza = seLanza
		if self.conquista == False: # and self.vida == True
			if seLanza:
				self.rect.top += 1
				if self.rect.left > jugador.rect.left:
					self.rect.left -= 1
				else:
					self.rect.left += 1

				if self.rect.left > self.resolución[0] or self.rect.top > self.resolución[1]:
					self.rect.top = 0
			else:
				self.__movimientos()

			self.__ataque()
			
			if self.tiempoCambio == round(tiempo):
				self.posImagen += 1
				self.tiempoCambio += 1

				if self.posImagen > len(self.listaimagenes)-1:
					self.posImagen = 0

		return tiempo2, índiceLance, id_objetivo

			
	def __ataque(self):
		#número_random_temporal = randint(1,450)
		if randint(1,450) <= self.rangoDisparo:
			self.__disparo()
	def __disparo(self):
		x,y = self.rect.center
		miProyectil = Proyectil(x,y,self.imagen_disparo, False)
		self.listadisparo.append(miProyectil)
		self.sonido_disparo.play()

	def __movimientos(self):
		self.movimientoLateral()

	def movimientoLateral(self):
		if self.derecha == True:
			self.rect.left = self.rect.left + self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False
		else:
			self.rect.left = self.rect.left - self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True
