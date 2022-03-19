import pygame
from Invasor import *
class Nave_nodriza(Invasor):
	def __init__(self,posx,posy,distancia, lista,tipo,resolución):
		super().__init__(posx,posy,distancia,lista,tipo,resolución)

		self.limiteDerecha = self.resolución[0] - self.listaimagenes[0].get_size()[0]
		print(self.listaimagenes[0].get_size()[0])
		self.limiteIzquierda = 0
		self.cant_vids = 10
		self.tiempo_rayo_comienzo = 1
		self.laser = pygame.Rect(0,0,0,0)
		self.tiempo_rayo = 0
		self.proyectiles = []
		self.img_orb = pygame.image.load('./Imagenes/enemigos/ORB_0.PNG').convert()

	def comportamiento(self, tiempo,tiempo2, ventana):
		self.movimientoLateral()

		if self.tiempoCambio == round(tiempo):
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaimagenes)-1:
				self.posImagen = 0

		if self.tiempo_rayo_comienzo == round(tiempo):
			self.tiempo_rayo_comienzo += 3
			self.tiempo_rayo = round(tiempo)

			for each in range(3):
				self.proyectiles.append(self.img_orb.get_rect(topleft=(self.rect.midbottom[0],self.rect.midbottom[1])))
				

		if tiempo > self.tiempo_rayo and tiempo < self.tiempo_rayo+1:
			self.__disparo(ventana)

		try:
			if self.proyectiles[0].top < self.resolución[1]:
				self.proyectiles[0].top += 5

			if self.proyectiles[1].top < self.resolución[1]:
				self.proyectiles[1].top += 5
				self.proyectiles[1].left -= 4

			if self.proyectiles[2].top < self.resolución[1]:
				self.proyectiles[2].top += 5
				self.proyectiles[2].left += 4

			for each in self.proyectiles:
				ventana.blit(self.img_orb,each)

				if each.top > self.resolución[1]:
					
					self.proyectiles = []

		except:
			pass

		return tiempo2

	def __disparo(self,ventana):
		self.laser = pygame.Rect(self.rect.midbottom[0],self.rect.midbottom[1],8, self.resolución[1])
		pygame.draw.rect(ventana,(135,206,235),self.laser)