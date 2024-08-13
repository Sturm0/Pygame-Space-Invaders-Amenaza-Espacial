import pygame
from time import time
class Explosion():
	def __init__(self,left,top,sonidoExplosion,imagenes):
		self.sonidoExplosion = sonidoExplosion
		self.imagenes = imagenes
		self.indice_fotograma_actual = 0
		self.imagen_actual = imagenes[self.indice_fotograma_actual]
		self.rect = self.imagen_actual.get_rect()
		self.rect.left = left
		self.rect.top = top
		self.tiempo_cambio = time()+0.025
		
		self.sonidoExplosion.play()
		#la idea es seguir creciendo esta clase para poner todo lo referente a explosiones que esta en main
	def comportamiento(self,tiempo,lista_explosiones):
		if self.indice_fotograma_actual < len(self.imagenes)-1:
			if time() >= self.tiempo_cambio:
				self.indice_fotograma_actual+=1
				self.imagen_actual = self.imagenes[self.indice_fotograma_actual]
		else:
			lista_explosiones.remove(self)
			
	def dibujar(self,superficie):
		superficie.blit(self.imagen_actual,(self.rect.left,self.rect.top))
		
