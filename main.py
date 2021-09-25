import pygame, sys
from pygame.locals import *
from time import sleep
from random import randint,uniform,choice
from os import system, name

def limpiar_pantalla():
	if name == "nt":
		system('cls')
	else:
		system('clear')
limpiar_pantalla()
#Variables globales
resolución = (1280,720)

class naveEspacial(pygame.sprite.Sprite):
	#clase para las naves
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load('Imagenes/SHIP.png')
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = resolución[0]/2
		self.rect.centery = resolución[1]-50
		self.listadisparo = []
		self.vida = True
	def disparar(self):
		pass
	def dibujar(self,superficie):
		superficie.blit(self.ImagenNave,self.rect)


def InvasionEspacial():
	pygame.init()
	pygame.mixer.init()
	#sonido = pygame.mixer.Sound("sonido.wav")
	#sonido.set_volume(0.5)
	#miFuente = pygame.font.Font('.ttf',20)
	ventana = pygame.display.set_mode(resolución) #,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED
	#ImagenFondo = pygame.image.load('Imagenes/Fondo.jpg')
	jugador = naveEspacial()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		ventana.fill((0,0,0))
		jugador.dibujar(ventana)
		#ventana.blit(ImagenFondo, (0,0))

		sleep(1/60)
		pygame.display.update()
InvasionEspacial()