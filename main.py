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
		self.ImagenNave = pygame.image.load('./Imagenes/SHIP.png')
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = resolución[0]/2
		self.rect.centery = resolución[1]-50
		self.listadisparo = []
		self.vida = True
		self.velocidad = 5

	# def movimientoDerecha(self):
	# 	self.rect.right += self.velocidad
	# 	self.__movimiento()

	# def movimientoIzquierda(self):
	# 	self.rect.left -= self.velocidad
	# 	self.__movimiento()

	def movimiento(self):
		if self.vida == True:
			if self.rect.left <= 0:
				self.rect.left = 0
			elif self.rect.left >= resolución[0]:
				self.rect.left = resolución[0]
			if self.rect.top < resolución[1] - resolución[1]/2:
				self.rect.top = resolución[1] - resolución[1]/2
	def disparar(self,x,y):
		print("Disparo")
		miProyectil = Proyectil(x,y)
		self.listadisparo.append(miProyectil)

	def dibujar(self,superficie):
		superficie.blit(self.ImagenNave,self.rect)

class Proyectil(pygame.sprite.Sprite):
	def __init__(self,posx,posy):
		pygame.sprite.Sprite.__init__(self)
		self.imageProyectil = pygame.image.load("Imagenes/SHOTS.png")
		self.rect = self.imageProyectil.get_rect()
		self.velocidadDisparo = 10
		self.rect.top = posy
		self.rect.left = posx
	def trayectoria(self):
		self.rect.top = self.rect.top - self.velocidadDisparo

	def dibujar(self,superficie):
		superficie.blit(self.imageProyectil,self.rect)

class Invasor(pygame.sprite.Sprite):
	def __init__(self,posx,posy):
		pygame.sprite.Sprite.__init__(self)
		self.imagenA = pygame.image.load("Imagenes/enemigos/ENEMY01.png")
		self.imagenB = pygame.image.load("Imagenes/enemigos/ENEMY02.png")
		self.imagenC = pygame.image.load("Imagenes/enemigos/ENEMY03.png")

		self.listaimagenes = [self.imagenA,self.imagenB,self.imagenC]
		self.posImagen = 0
		self.imagenInvasor = self.listaimagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()
		self.listadisparo = []
		self.velocidad = 20
		self.rect.top = posy
		self.rect.left = posx

		self.tiempoCambio = 1
	def trayectoria(self):
		self.rect.top = self.rect.top - self.velocidadDisparo

	def dibujar(self,superficie):
		self.imagenInvasor = self.listaimagenes[self.posImagen]
		superficie.blit(self.imagenInvasor,self.rect)

	def comportamiento(self,tiempo):
		if self.tiempoCambio == round(tiempo):
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaimagenes)-1:
				self.posImagen = 0

def InvasionEspacial():
	pygame.init()
	#sonido = pygame.mixer.Sound("sonido.wav")
	#sonido.set_volume(0.5)
	#miFuente = pygame.font.Font('.ttf',20)
	ventana = pygame.display.set_mode(resolución) #,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED
	#ImagenFondo = pygame.image.load('Imagenes/Fondo.jpg')
	jugador = naveEspacial()
	enemigo = Invasor(100,100)
	enJuego = True
	acumulador = 0
	reloj = pygame.time.Clock()
	while True:
		
		tiempo = pygame.time.get_ticks()/1000
		jugador.movimiento()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		#Acá se configura la asignación de teclas
		keys = pygame.key.get_pressed()

		if enJuego == True and 1 in keys:
			if keys[K_UP] and keys[K_SPACE]:
				jugador.rect.top -= jugador.velocidad
				x,y = jugador.rect.center
				jugador.disparar(x,y)
				if acumulador == 10:
					
					acumulador = 0
				acumulador += 1

			elif keys[K_DOWN] and keys[K_SPACE]:
				jugador.rect.top += jugador.velocidad
				x,y = jugador.rect.center
				jugador.disparar(x,y)
				if acumulador == 10:
					
					acumulador = 0
				acumulador += 1

			if keys[K_RIGHT] and keys[K_SPACE]:
				jugador.rect.left += jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y)
					
					acumulador = 0
				acumulador += 1

			elif keys[K_LEFT] and keys[K_SPACE]:
				jugador.rect.left -= jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y)
					
					acumulador = 0
				acumulador += 1

			elif keys[K_UP]:
				jugador.rect.top -= jugador.velocidad
			elif keys[K_DOWN]:
				jugador.rect.top += jugador.velocidad
			elif keys[K_RIGHT]:
				jugador.rect.left += jugador.velocidad
			elif keys[K_LEFT]:
				jugador.rect.left -= jugador.velocidad
			elif keys[K_SPACE]:
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y)
					
					acumulador = 0
				acumulador += 1

		ventana.fill((0,0,0))
		
		
		#demoProyectil.dibujar(ventana)
		#ventana.blit(ImagenFondo, (0,0))
		if len(jugador.listadisparo) > 0:
			for x in jugador.listadisparo:
				x.dibujar(ventana)
				x.trayectoria()
				if x.rect.top < 0: #para que se elimnen las balas cuando no están en la ventana
					jugador.listadisparo.remove(x)
		enemigo.comportamiento(tiempo)			
		jugador.dibujar(ventana)
		enemigo.dibujar(ventana)

		#sleep(1/60)
		#pygame.time.wait(round((1/60)*1000))
		reloj.tick(60)
		pygame.display.update()
		print(f"{reloj.get_fps():.2f}")
InvasionEspacial()