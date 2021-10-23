import pygame, sys
from pygame.locals import *
from time import sleep, time
from random import randint,uniform,choice
from os import system, name
from random import randint
from copy import deepcopy 
def limpiar_pantalla():
	if name == "nt":
		system('cls')
	else:
		system('clear')
limpiar_pantalla()
pygame.init()
resolución = (1280,720)
ventana = pygame.display.set_mode(resolución) #,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED
#Variables globales
jej_temporal = True #ESTO ES PARA PRUEBAS ES RELEVANTE REMOVERLA LUEGO DE HABERLAS HECHO
tiempo_muerte = 0
listaEnemigo = []
#explosion = pygame.image.load('./Imagenes/EXPLODE/EXPLODE_medio.png')
explosion = []
niv_objetivo = 0
niv = 0
for each in ['./Imagenes/EXPLODE/EXPLODE%s.png'%x for x in range(1,21)]: #'./Imagenes/EXPLODE/EXPLODE_medio.png'ahora esta puesto ese None para que lo interprete como una lista, luego sera agregado cada frame de la explosión
	print(each)
	if each != None:
		explosion.append(pygame.image.load(each).convert())

class naveEspacial(pygame.sprite.Sprite):
	#clase para las naves
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load('./Imagenes/SHIP.png').convert()
		#self.ImagenExplosion = pygame.image.load('./Imagenes/EXPLODE/EXPLODE_medio.png')
		self.ImagenExplosion = explosion[0]
		#self.sonidoExplosion = pygame.mixer.Sound()
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = resolución[0]/2
		self.rect.centery = resolución[1]-50
		self.listadisparo = []
		self.vidas = 3
		self.vida = True
		self.velocidad = 5
		self.puntaje = 0
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

	

	def destruccion(self):
		#self.sonidoExplosion.play()
		
		self.vidas -= 1
		if self.vidas < 1:
			self.Vida = False
		#print(self.vidas)
		self.velocidad = 0
		self.ImagenNave = self.ImagenExplosion

	def revivir(self):
		self.velocidad = 5
		self.ImagenNave = pygame.image.load('./Imagenes/SHIP.png').convert()
		self.rect.centerx = resolución[0]/2
		self.rect.centery = resolución[1]-50

	def dibujar(self,superficie):
		superficie.blit(self.ImagenNave,self.rect)

class Proyectil(pygame.sprite.Sprite):
	def __init__(self,posx,posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)
		self.imageProyectil = pygame.image.load(ruta).convert() #"Imagenes/SHOTS.png"
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
		self.ImagenExplosion = explosion
		self.listaimagenes = [self.imagenA,self.imagenB,self.imagenC]
		self.posImagen = 0
		self.posImagen2 = 0
		self.imagenInvasor = self.listaimagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()
		self.listadisparo = []
		self.velocidad = 2
		self.rect.top = posy
		self.rect.left = posx
		self.rangoDisparo = 1 #Determina la probabilidad de disparo
		self.tiempoCambio = 3
		self.tiempoCambio2 = 0.025 #todavía no hago nada con esto
		self.conquista = False
		self.derecha = True
		self.contador = 0
		self.Maxdescenso = self.rect.top + 40
		self.vida = True 
		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx #- distancia
		#self.sonidoExplosion = pygame.mixer.Sound('./Sonidos/EXPLODE.WAV')
	def trayectoria(self):
		self.rect.top = self.rect.top - self.velocidadDisparo

	def dibujar(self,superficie):
		if self.vida == True:
			self.imagenInvasor = self.listaimagenes[self.posImagen]
		else:
			#acá se muestra la explosión del invasor
			#self.tiempo1 = time()
			self.imagenInvasor = self.ImagenExplosion[self.posImagen2]
			

		superficie.blit(self.imagenInvasor,self.rect)

	def comportamiento(self,tiempo,tiempo2):
		#algoritmo de comportamiento
		if self.conquista == False and self.vida == True:
			self.__movimientos()
			self.__ataque()
			#if self.tiempoCambio == tiempo or (self.tiempoCambio < tiempo+0.016 and self.tiempoCambio > tiempo+0.016):
			#print(self.tiempoCambio,tiempo,round(tiempo))
			if self.tiempoCambio == round(tiempo):
				#print("Entro"+str(randint(0,500)))
				self.posImagen += 1
				self.tiempoCambio += 1


				if self.posImagen > len(self.listaimagenes)-1:
					self.posImagen = 0
		elif self.vida == False:
			#Esto esta para que se pueda ver la explosión
			if time() > tiempo2+0.5:
				listaEnemigo.remove(self)
				self.posImagen2 = 0
			else:
				if self.posImagen2 < len(self.ImagenExplosion)-1 and time() >= tiempo2+self.tiempoCambio2:
					self.posImagen2 += 1
					self.tiempoCambio2 += 0.025
				#revisar esta porción de código
				# if time() >= tiempo2+0.14:
				# 	if self.posImagen2 < len(self.ImagenExplosion)-1:
				# 		self.posImagen2 += 1
				# 	tiempo2 += 0.14
					
		return tiempo2
			
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

	# def morir(self):
	# 	self.vida = False
		#listaEnemigo.remove(self)

class Asteroide(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.listaimagenes = []

def detenerTodo(*args):
	# if args == "Jugador pasa de nivel":
	# 	niv = True 
	for enemigo in listaEnemigo:
		for disparo in enemigo.listadisparo:
			enemigo.listadisparo.remove(disparo)
		enemigo.conquista = True
	# return niv

def cargarEnemigos():

	lista_y = [20,120,220]
	posx = 100
	for cada_uno in lista_y:
		for x in range(1,10):
			enemigo = Invasor(posx,cada_uno,300,"Imagenes/enemigos/ENEMY01.png","Imagenes/enemigos/ENEMY02.png","Imagenes/enemigos/ENEMY03.png")
			print(enemigo.tiempoCambio)
			listaEnemigo.append(enemigo)
			posx += 75
			if x == 9:
				posx = 100

def InvasionEspacial():
	global jej_temporal
	global niv
	global listaEnemigo
	global tiempo_muerte

	tiempo2 = None
	sonido = pygame.mixer.Sound("./Sonidos/space.ogg")
	sonidoExplosion = pygame.mixer.Sound('./Sonidos/EXPLODE.WAV')
	sonido.play()
	gameover = pygame.image.load('./Imagenes/gameover.bmp').convert()
	gameover = pygame.transform.scale(gameover,(resolución[0],resolución[1]))

	#Fuentes
	miFuente = pygame.font.Font(None,20)
	miFuenteFin = pygame.font.Font(None,90)
	miFuenteNivel = pygame.font.Font(None,50)
	Texto = miFuenteFin.render("Fin del juego",0,(120,100,40))

	#ImagenFondo = pygame.image.load('Imagenes/Fondo.jpg')
	jugador = naveEspacial()
	TextoPuntaje = miFuente.render("Puntuación: "+str(jugador.puntaje),0,(255,255,255))
	TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
	
	cargarEnemigos()

	enJuego = True
	acumulador = 0
	tiempo_niv = 0
	reloj = pygame.time.Clock()
	nuev_niv = [False,0]

	#Generación de estrellas
	listaEstrellas = [[],[],[]]
	for cada_elemento in range(0,3):
		for each in range(1,41):
			x_aleatorio = randint(0,resolución[0])
			y_aleatorio = randint(0,resolución[1])
			listaEstrellas[cada_elemento].append([x_aleatorio,y_aleatorio])
	#mandioca = 0
	tiempo256 = 0
	while True:
		
		tiempo = (pygame.time.get_ticks()/1000)-tiempo256
		#print("TIEMPO: ",tiempo,tiempo-mandioca)
		#mandioca = tiempo
		jugador.movimiento()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if len(listaEnemigo) <= 1:
						cargarEnemigos()
						tiempo256 = pygame.time.get_ticks()/1000
						jugador.revivir()
						if jej_temporal:
							niv += 1
						else:
							jej_temporal = True

		#Acá se configura la asignación de teclas
		keys = pygame.key.get_pressed()

		if enJuego == True and 1 in keys:
			#Parece que siempre hay al menos uno de estos que no se activa aunque supuestamente debería
			#print(bool(keys[K_LEFT]),bool(keys[K_UP]),bool(keys[K_SPACE]))

			if keys[K_RIGHT] and keys[K_SPACE] and keys[K_UP]:
				jugador.rect.left += jugador.velocidad
				jugador.rect.top -= jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y)
					
					acumulador = 0
				acumulador += 1

			#problemas acá no entra
			elif bool(keys[K_LEFT]) and bool(keys[K_UP]) and keys[K_SPACE]:
				jugador.rect.left -= jugador.velocidad
				jugador.rect.top -= jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y)
					
					acumulador = 0
				acumulador += 1

			elif keys[K_UP] and keys[K_SPACE]:
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

			elif keys[K_RIGHT] and keys[K_SPACE]:
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
			elif keys[K_UP] and keys[K_LEFT]:
				jugador.rect.top -= jugador.velocidad
				jugador.rect.left -= jugador.velocidad

			elif keys[K_UP] and keys[K_RIGHT]:
				jugador.rect.top -= jugador.velocidad
				jugador.rect.left += jugador.velocidad
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
		#pygame.draw.rect(ventana, (255,0,0), (resolución[0]/2,resolución[1]/2,4,4))
		velocidades = (1,2,3)
		for índice_main,elemento in enumerate(velocidades,0):
			for índice, each in enumerate(listaEstrellas[índice_main],0):
				if each[1] < resolución[1]:
					listaEstrellas[índice_main][índice][1] += elemento
					pygame.draw.rect(ventana, (255,255,255), (each[0],each[1],1,1))
				else:
					pygame.draw.rect(ventana, (255,255,255), (each[0],0,1,1))
					listaEstrellas[índice_main][índice][1] = 0
	

		if len(listaEnemigo) > 0:

			for enemigo in listaEnemigo:

				tiempo2 = enemigo.comportamiento(tiempo,tiempo2)
				enemigo.dibujar(ventana)

				if enemigo.rect.colliderect(jugador.rect):
					jugador.destruccion()
					enJuego = False
					detenerTodo()

				if len(enemigo.listadisparo) > 0:

					for x in enemigo.listadisparo:
						
						x.dibujar(ventana)
						x.trayectoria()
						if x.rect.colliderect(jugador.rect):
							jugador.destruccion()
							enemigo.listadisparo.remove(x)
							tiempo_muerte = time()
							listaEnemigo = []
							jej_temporal = False
							TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(120,100,40))
							if jugador.vidas < 1:
								print("entro acá")
								enJuego = False
								detenerTodo()
						if x.rect.top > resolución[1]:
							enemigo.listadisparo.remove(x)
				
		else:
			#print("Entro en este otro lugar")
			tiempo_niv = time() #la hora cuando se muestra el cártel que indica que pasaste de nivel
			
			# if time() > tiempo_muerte+2:
			# 	cargarEnemigos()
			# 	jugador.revivir()
			# 	niv += 1
			TextoNivel = miFuenteNivel.render("Nivel: "+str(niv),0,(255,255,255))
			TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
			tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
			ventana.blit(TextoNivel,((resolución[0]/2)-tamaño_texto[0]/2,(resolución[1]/2)-(tamaño_texto[1]/2)))
			ventana.blit(TextoNivelB,((resolución[0]/2)-tamaño_texto[0]/2,(resolución[1]/2)-(tamaño_texto[1]/2)+50))
			
			nuev_niv = [True, 0]

		
		if len(jugador.listadisparo) > 0:
			for x in jugador.listadisparo:
				x.dibujar(ventana)
				x.trayectoria()

				if x.rect.top < 0: #para que se elimnen las balas cuando no están en la ventana
					jugador.listadisparo.remove(x)
				else:
					for enemigo in listaEnemigo:
						if x.rect.colliderect(enemigo.rect) and enemigo.vida:
							
							enemigo.vida = False
							#if x in jugador.listadisparo:
							
							jugador.listadisparo.remove(x)

							#SI NO SE LOGRA LO DEL ANTERIOR COMENTARIO INEVITABLEMENTE EL SONIDO SE VA A ESCUCHAR MAL
							sonidoExplosion.play()
							jugador.puntaje += 100
							TextoPuntaje = miFuente.render("Puntuación: "+str(jugador.puntaje),0,(255,255,255))
							tiempo2 = time()
			
		ventana.blit(TextoPuntaje,(30,resolución[1]-30))
		ventana.blit(TextoVidas,(resolución[0]-70,resolución[1]-30))
		
		jugador.dibujar(ventana)
		

		if enJuego == False:
			pygame.mixer.music.fadeout(3000) #se detiene en 3 segundos de forma paulatina
			ventana.blit(gameover,(0,0))
			#ventana.blit(Texto,(resolución[0]/2,resolución[1]/2))


		#print(niv)
		reloj.tick(60)
		pygame.display.update()
		#print(f"{reloj.get_fps():.2f}")

InvasionEspacial()