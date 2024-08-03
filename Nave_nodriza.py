import pygame
from Invasor import *
from time import  time
from Orbe import *
class Nave_nodriza(Invasor):
	def __init__(self,posx,posy,distancia, lista,tipo,resolución):
		super().__init__(posx,posy,distancia,lista,tipo,resolución)

		self.limiteDerecha = self.resolución[0] - self.listaimagenes[0].get_size()[0]
		print(self.listaimagenes[0].get_size()[0])
		self.limiteIzquierda = 0
		self.cant_vids = 10
		self.tiempo_rayo_comienzo = 1
		self.laser = pygame.Rect(self.rect.midbottom[0],self.rect.midbottom[1],8,self.resolución[1]/3)
		self.tiempo_rayo = 0
		self.lista_orbes = []
		self.sonido_laser = pygame.mixer.Sound('./Sonidos/LASER.WAV')
		
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

			self.lista_orbes.append(Orbe((self.rect.midbottom[0],self.rect.midbottom[1]),"izquierda"))
			self.lista_orbes.append(Orbe((self.rect.midbottom[0],self.rect.midbottom[1]),"centro"))
			self.lista_orbes.append(Orbe((self.rect.midbottom[0],self.rect.midbottom[1]),"derecha"))
			self.lista_orbes[0].sonido.play()
			self.sonido_laser.play()

		if tiempo > self.tiempo_rayo and tiempo < self.tiempo_rayo+1:
			self.__disparo(ventana)
		else:
			self.laser.topleft = (0,0)
			self.laser.height = self.resolución[1]/3
				
		for each in self.lista_orbes:
			each.update()
			each.dibujar(ventana)
			if each.rect.top > self.resolución[1]:
				self.lista_orbes = []

		return tiempo2

	def __disparo(self,ventana):
		self.laser.left = self.rect.midbottom[0]
		self.laser.top = self.rect.midbottom[1]
		self.laser.height += 4
		pygame.draw.rect(ventana,(135,206,235),self.laser)
		
