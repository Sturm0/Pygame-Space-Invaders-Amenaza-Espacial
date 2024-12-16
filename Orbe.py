import pygame
from time import  time

class Orbe():
	def __init__(self,topleft,direccion):
		self.direccion = direccion		
		self.velocidad_vertical = 4
		self.velocidad_horizontal = 3 
		
		self.img_orbes = pygame.image.load('./Imagenes/enemigos/ORB.PNG').convert()
		self.orbe = pygame.Surface((64, 64))
		
		self.rect = self.orbe.get_rect()
		self.rect.topleft = topleft
		
		self.orbe.blit(self.img_orbes,(0,0))
		
		self.orbe_inicio = 0 #indica cuantos pixeles a la izquierda está el origen en la imagen ORB.PNG (para poder ir seleccionando los distintos estados del orbe)
		self.tiempo_cambio_orbe = time()+.03
		
		self.sonido = pygame.mixer.Sound('./Sonidos/PULSE.WAV')
		
	def update(self):		
		self.rect.top += self.velocidad_vertical
		if self.direccion == "izquierda":
			self.rect.left -= self.velocidad_horizontal
		elif self.direccion == "derecha":
			self.rect.left += self.velocidad_horizontal
				
	def dibujar(self,ventana):
		if time() > self.tiempo_cambio_orbe:
				self.orbe.blit(self.img_orbes,(0,0),(self.orbe_inicio,0,64,64))
				self.orbe_inicio += 64
				self.tiempo_cambio_orbe += .03
			
		if self.orbe_inicio > 576:
			self.orbe_inicio = 0
		ventana.blit(self.orbe,self.rect)
		
	def recibir_disparo(self,jugador,jugador_disparo):
		try:
			jugador.listadisparo.remove(jugador_disparo)
		except:
			pass
