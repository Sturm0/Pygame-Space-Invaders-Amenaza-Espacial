import pygame
class Proyectil():
	def __init__(self,posx,posy, imageProyectil, personaje):
		pygame.sprite.Sprite.__init__(self)
		# ~ self.imageProyectil = pygame.image.load(ruta).convert()
		self.imageProyectil = imageProyectil
		self.rect = self.imageProyectil.get_rect()
		self.rect.top = posy
		self.rect.left = posx
		self.velocidadDisparo = 5
		self.disparoPersonaje = personaje

	def trayectoria(self):
		if self.disparoPersonaje:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def dibujar(self,superficie):
		superficie.blit(self.imageProyectil,self.rect)
