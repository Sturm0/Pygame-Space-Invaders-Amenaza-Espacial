import pygame
from Asteroide import Asteroide
class Potenciadores(pygame.sprite.Sprite):
	def __init__(self,índice,x,y,ImagenesPotenciadores,sonido):
		pygame.sprite.Sprite.__init__(self)
		self.potenciador = ImagenesPotenciadores[índice]
		self.rect = self.potenciador.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.tipo = índice
		self.sonido = sonido
	def dibujar(self,ventana):
		ventana.blit(self.potenciador,self.rect)
	def mover(self):
		self.rect.top += Asteroide.velocidad
