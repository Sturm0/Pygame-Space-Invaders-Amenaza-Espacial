import pygame, sys
from pygame.locals import *
from time import sleep
from random import randint,uniform,choice
from os import system, name
from random import randint

def limpiar_pantalla():
	if name == "nt":
		system('cls')
	else:
		system('clear')
limpiar_pantalla()
#Variables globales
resolución = (1280,720)
listaEnemigo = []
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
		miProyectil = Proyectil(x,y,"Imagenes/SHOTS.png",True)
		self.listadisparo.append(miProyectil)

	def dibujar(self,superficie):
		superficie.blit(self.ImagenNave,self.rect)

class Proyectil(pygame.sprite.Sprite):
	def __init__(self,posx,posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)
		self.imageProyectil = pygame.image.load(ruta) #"Imagenes/SHOTS.png"
		self.rect = self.imageProyectil.get_rect()
		self.velocidadDisparo = 5
		self.rect.top = posy
		self.rect.left = posx

		self.disparoPersonaje = personaje
	def trayectoria(self):
		if self.disparoPersonaje == True:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def dibujar(self,superficie):
		superficie.blit(self.imageProyectil,self.rect)

class Invasor(pygame.sprite.Sprite):
	def __init__(self,posx,posy,distancia, ImagenUno, ImagenDos, ImagenTres):
		pygame.sprite.Sprite.__init__(self)
		self.imagenA = pygame.image.load(ImagenUno)
		self.imagenB = pygame.image.load(ImagenDos)
		self.imagenC = pygame.image.load(ImagenTres)
		self.listaimagenes = [self.imagenA,self.imagenB,self.imagenC]
		self.posImagen = 0
		self.imagenInvasor = self.listaimagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()
		self.listadisparo = []
		self.velocidad = 2
		self.rect.top = posy
		self.rect.left = posx
		self.rangoDisparo = 1 #Determina la probabilidad de disparo
		self.tiempoCambio = 3

		self.derecha = True
		self.contador = 0
		self.Maxdescenso = self.rect.top + 40

		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx #- distancia
	def trayectoria(self):
		self.rect.top = self.rect.top - self.velocidadDisparo

	def dibujar(self,superficie):
		self.imagenInvasor = self.listaimagenes[self.posImagen]
		superficie.blit(self.imagenInvasor,self.rect)

	def comportamiento(self,tiempo):
		#algoritmo de comportamiento
		self.__movimientos()
		self.__ataque()
		print(self.tiempoCambio,tiempo)
		if self.tiempoCambio == round(tiempo):
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaimagenes)-1:
				self.posImagen = 0

	def __ataque(self):
		número_random_temporal = randint(1,450)
		#print(número_random_temporal)
		if número_random_temporal == self.rangoDisparo:
			self.__disparo()
	def __disparo(self):
		x,y = self.rect.center
		miProyectil = Proyectil(x,y,"Imagenes/enemigos/ESHOT_0.png", False)
		self.listadisparo.append(miProyectil)

	def __movimientos(self):
		self.__movimientoLateral()

		#Bloque todavía no implementado
		# if self.contador < 3:
		# 	self.__movimientoLateral()
		# else:
		# 	self.__descenso()

	# def __descenso(self):
	# 	if self.Maxdescenso == self.rect.top:
	# 		self.contador = 0
	# 		self.Maxdescenso = self.rect.top + 40
	# 	else:
	# 		self.rect.top += 1

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left = self.rect.left + self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False
				#self.contador += 1
		else:
			self.rect.left = self.rect.left - self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True
				#self.contador += 1

def cargarEnemigos():

	
	lista_y = [20,120,220]
	posx = 100
	for cada_uno in lista_y:
		for x in range(1,10):
			enemigo = Invasor(posx,cada_uno,300,"Imagenes/enemigos/ENEMY01.png","Imagenes/enemigos/ENEMY02.png","Imagenes/enemigos/ENEMY03.png")
			listaEnemigo.append(enemigo)
			posx += 75
			if x == 9:
				posx = 100
				
def InvasionEspacial():
	pygame.init()
	sonido = pygame.mixer.Sound("./Sonidos/space.ogg")
	#sonido.play()
	
	#miFuente = pygame.font.Font('.ttf',20)
	ventana = pygame.display.set_mode(resolución) #,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED
	#ImagenFondo = pygame.image.load('Imagenes/Fondo.jpg')
	jugador = naveEspacial()
	cargarEnemigos()

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
		if len(listaEnemigo) > 0:
			for enemigo in listaEnemigo:
				enemigo.comportamiento(tiempo)
				enemigo.dibujar(ventana)

				if len(enemigo.listadisparo) > 0:
					for x in enemigo.listadisparo:
						x.dibujar(ventana)
						x.trayectoria()
						if x.rect.top > resolución[1]:
							enemigo.listadisparo.remove(x)

		if len(jugador.listadisparo) > 0:
			for x in jugador.listadisparo:
				x.dibujar(ventana)
				x.trayectoria()
				if x.rect.top < 0: #para que se elimnen las balas cuando no están en la ventana
					jugador.listadisparo.remove(x)

		jugador.dibujar(ventana)
		reloj.tick(60)
		pygame.display.update()
		#print(f"{reloj.get_fps():.2f}")
InvasionEspacial()