import pygame
from Proyectil import *
from pygame.locals import *
from pathlib import Path
class naveEspacial():
	#clase para las naves
	def __init__(self,explosion,resolución,disparos_jugador,asignaciones=[K_UP,K_DOWN,K_RIGHT,K_LEFT,K_SPACE]):

		pygame.sprite.Sprite.__init__(self)
		self.resolución = resolución
		self.ImagenNave = pygame.image.load(Path(__file__).parent/'Imagenes/SHIP.png').convert()
		self.ImagenExplosion = explosion[0]
		#self.sonidoExplosion = pygame.mixer.Sound()
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = self.resolución[0]/2
		self.rect.centery = self.resolución[1]-50
		self.listadisparo = []
		self.vidas = 4
		self.vida = True
		self.eliminado = False
		self.velocidad = 4
		self.puntaje = 0
		self.sonidoDisparo = pygame.mixer.Sound(Path(__file__).parent/'Sonidos/SHOT1.WAV')
		self.sonido_laser = pygame.mixer.Sound(Path(__file__).parent/'Sonidos/LASER.WAV')
		self.asignaciones = asignaciones
		self.acumulador = 0
		self.potenciador_val = -1
		self.disparos_jugador = disparos_jugador

	def movimiento(self):
		if self.vida == True:
			if self.rect.left <= 0:
				self.rect.left = 0
			#elif self.rect.left >= self.resolución[0]:
				#self.rect.left = self.resolución[0]
				#pass
			if self.rect.top < self.resolución[1] - self.resolución[1]/2:
				self.rect.top = self.resolución[1] - self.resolución[1]/2
			elif self.rect.top > self.resolución[1]:
				self.rect.top = self.resolución[1]
	def disparar(self,x,y,potenciador_valor):
		if potenciador_valor == -1:
			miProyectil = Proyectil(x,y,self.disparos_jugador[0],True)
			
			self.sonidoDisparo.play()
		elif potenciador_valor == 0:
			miProyectil = Proyectil(x-8,y,self.disparos_jugador[1],True)
			miProyectil2 = Proyectil(x+5,y,self.disparos_jugador[1],True)
			self.listadisparo.append(miProyectil2)
			self.sonidoDisparo.play()
		elif potenciador_valor == 1:
			miProyectil = Proyectil(x-8,y,self.disparos_jugador[2],True)
			self.sonidoDisparo.play()
			for index,each in enumerate([Proyectil(x+5,y,self.disparos_jugador[2],True),Proyectil(x,y,self.disparos_jugador[2],True)],0):
				self.listadisparo.append(each)
				if index == 1:
					each.velocidadDisparo -= 1

		self.listadisparo.append(miProyectil)


	def destruccion(self):
		self.vidas -= 1
		if self.vidas < 1:
			self.Vida = False
		self.velocidad = 0
		self.ImagenNave = self.ImagenExplosion

	def revivir(self):
		self.velocidad = 5
		self.ImagenNave = pygame.image.load(Path(__file__).parent/'Imagenes/SHIP.png').convert()
		self.rect.centerx = self.resolución[0]/2
		self.rect.centery = self.resolución[1]-50

	def dibujar(self,superficie,vida=True):
		if vida:
			superficie.blit(self.ImagenNave,self.rect)

	def entrada(self,teclas):
		#sirve para leer la entrada del jugador y actuar acorde
		if teclas[self.asignaciones[0]]:
			self.rect.top -= self.velocidad
		if teclas[self.asignaciones[1]]:
			self.rect.top += self.velocidad
		if teclas[self.asignaciones[2]]:
			self.rect.left += self.velocidad
		if teclas[self.asignaciones[3]]:
			self.rect.left -= self.velocidad
		if teclas[self.asignaciones[4]]:
			x,y = self.rect.center
			if self.acumulador == 10:
				self.disparar(x,y,self.potenciador_val)
				self.acumulador = 0
			self.acumulador += 1
		pass
