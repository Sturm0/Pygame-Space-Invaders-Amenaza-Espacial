import pygame
from random import randint
class Asteroide(pygame.sprite.Sprite):
	velocidad = 5
	def __init__(self,posx,posy):
		pygame.sprite.Sprite.__init__(self)
		self.listaimagenes = []
		self.vida = True
		for each in ['./Imagenes/Asteroides/ASTEROID%s.PNG'%x for x in range(0,5)]:
			if each != None:
				self.listaimagenes.append(pygame.image.load(each).convert())
		self.rand = randint(0,3)
		self.rect = self.listaimagenes[self.rand].get_rect()
		self.rect.left = posx
		self.rect.top = posy

	def dibujar(self,superficie):
		superficie.blit(self.listaimagenes[self.rand],(self.rect.left,self.rect.top))