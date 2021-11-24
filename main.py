import pygame, sys
from pygame.locals import *
from time import sleep, time
from random import randint,uniform,choice
from os import system, name
from random import randint
from copy import deepcopy 
from timeit import timeit
from functools import lru_cache
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

listaEnemigo = []
explosion = []
id_objetivo = None
niv_objetivo = 0
niv = 0
#Carga de imagenes
for each in ['./Imagenes/EXPLODE/EXPLODE%s.PNG'%x for x in range(1,21)]:
	print(each)
	if each != None:
		explosion.append(pygame.image.load(each).convert())
listaPotenciadores = []
for each in ['./Imagenes/Potenciadores/Potenciador%s.PNG'%x for x in range(0,1)]:
	print(each)
	if each != None:
		listaPotenciadores.append(pygame.image.load(each).convert())

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
		self.eliminado = False
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
	def disparar(self,x,y,potenciador_valor):
		if potenciador_valor == 0:
			miProyectil = Proyectil(x,y,"Imagenes/SHOTS.png",True)
		elif potenciador_valor == 1:
			miProyectil = Proyectil(x-8,y,"Imagenes/SHOTS2.png",True)
			miProyectil2 = Proyectil(x+5,y,"Imagenes/SHOTS2.png",True)
			self.listadisparo.append(miProyectil2)
		self.listadisparo.append(miProyectil)

	def destruccion(self):
		#self.sonidoExplosion.play()
		
		self.vidas -= 1
		if self.vidas < 1:
			self.Vida = False
		self.velocidad = 0
		self.ImagenNave = self.ImagenExplosion

	def revivir(self):
		self.velocidad = 5
		self.ImagenNave = pygame.image.load('./Imagenes/SHIP.png').convert()
		self.rect.centerx = resolución[0]/2
		self.rect.centery = resolución[1]-50

	def dibujar(self,superficie,vida=True):
		if vida:
			superficie.blit(self.ImagenNave,self.rect)

class Proyectil(pygame.sprite.Sprite):
	def __init__(self,posx,posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)
		self.imageProyectil = pygame.image.load(ruta).convert() #"Imagenes/SHOTS.png"
		self.rect = self.imageProyectil.get_rect()
		self.rect.top = posy
		self.rect.left = posx
		# if potenciador_valor == 1:
		# 	self.rect2 = self.imageProyectil.get_rect()
		# 	self.rect2.top = posy
		# 	self.rect2.left = posx+30
		# 	self.rect.left = posx-8
		self.velocidadDisparo = 5
		self.disparoPersonaje = personaje

	def trayectoria(self):
		if self.disparoPersonaje == True:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def dibujar(self,superficie):
		superficie.blit(self.imageProyectil,self.rect)

class Invasor(pygame.sprite.Sprite):
	def __init__(self,posx,posy,distancia, lista,tipo):
		pygame.sprite.Sprite.__init__(self)
		
		self.listaimagenes = [] 
		for each in lista:
			self.listaimagenes.append(pygame.image.load(each))

		if tipo == 1:
			self.imagen_disparo = "Imagenes/enemigos/ESHOT_1.png"	
		else:
			self.imagen_disparo = "Imagenes/enemigos/ESHOT_0.png"

		self.ImagenExplosion = explosion
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
		self.seLanza = False
	def trayectoria(self):
		#self.rect.top = self.rect.top - self.velocidadDisparo
		pass

	def dibujar(self,superficie):
		if self.vida == True:
			self.imagenInvasor = self.listaimagenes[self.posImagen]
		else:
			#acá se muestra la explosión del invasor
			#self.tiempo1 = time()
			self.imagenInvasor = self.ImagenExplosion[self.posImagen2]
			

		superficie.blit(self.imagenInvasor,self.rect)

	def comportamiento(self,tiempo,tiempo2,seLanza,índiceLance,jugador,id_objetivo):
		#algoritmo de comportamiento
		self.seLanza = seLanza
		if self.conquista == False and self.vida == True:
			if seLanza:
				self.rect.top += 1
				if self.rect.left > jugador.rect.left:
					self.rect.left -= 1
				else:
					self.rect.left += 1

				if self.rect.left > resolución[0] or self.rect.top > resolución[1]:
					#self.vida = False
					self.rect.top = 0
			else:
				self.__movimientos()

			self.__ataque()
			
			if self.tiempoCambio == round(tiempo):
				self.posImagen += 1
				self.tiempoCambio += 1

				if self.posImagen > len(self.listaimagenes)-1:
					self.posImagen = 0
		elif self.vida == False:

			if time() > tiempo2+0.5:
				listaEnemigo.remove(self)
				self.posImagen2 = 0
				if seLanza and len(listaEnemigo) > 0:
					índiceLance = randint(0,len(listaEnemigo)-1)
					id_objetivo = id(listaEnemigo[índiceLance])
			else:
				if self.posImagen2 < len(self.ImagenExplosion)-1 and time() >= tiempo2+self.tiempoCambio2:
					self.posImagen2 += 1
					self.tiempoCambio2 += 0.025

		return tiempo2, índiceLance, id_objetivo

			
	def __ataque(self):
		número_random_temporal = randint(1,450)
		#print(número_random_temporal)
		if número_random_temporal == self.rangoDisparo:
			self.__disparo()
	def __disparo(self):
		x,y = self.rect.center
		miProyectil = Proyectil(x,y,self.imagen_disparo, False)
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
		#superficie.blit(self.listaimagenes[self.posImagen],(self.posx,self.posy))
		#superficie.blit(self.listaimagenes[self.posImagen],(self.rect.left,self.rect.top))
		superficie.blit(self.listaimagenes[self.rand],(self.rect.left,self.rect.top))

class Potenciadores(pygame.sprite.Sprite):
	def __init__(self,índice,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.potenciador = listaPotenciadores[índice]
		self.rect = self.potenciador.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.tipo = índice
	def dibujar(self,ventana):
		ventana.blit(self.potenciador,self.rect)
	def mover(self):
		self.rect.top += Asteroide.velocidad
def detenerTodo(*args):
	# if args == "Jugador pasa de nivel":
	# 	niv = True 
	for enemigo in listaEnemigo:
		for disparo in enemigo.listadisparo:
			enemigo.listadisparo.remove(disparo)
		enemigo.conquista = True
	# return niv

#se podría agregar un decorador cache a esta función para hacerla más rápida
#@lru_cache(maxsize=2)
def cargarEnemigos(tipo):
	lista_y = [20,120,220]
	posx = 100
	if tipo == 0:
		for cada_uno in lista_y:
			for x in range(1,10):
				enemigo = Invasor(posx,cada_uno,200,["Imagenes/enemigos/ENEMY01.png","Imagenes/enemigos/ENEMY02.png","Imagenes/enemigos/ENEMY03.png"],0)
				#print(enemigo.tiempoCambio)
				listaEnemigo.append(enemigo)
				posx += 75
				if x == 9:
					posx = 100
	else:
		for cada_uno in lista_y:
			for x in range(1,10):
				#enemigo = Invasor(posx,cada_uno,200,["Imagenes/enemigos/ENEMY2_1.PNG","Imagenes/enemigos/ENEMY2_2.PNG","Imagenes/enemigos/ENEMY2_3.PNG","Imagenes/enemigos/ENEMY2_4.PNG"])
				enemigo = Invasor(posx,cada_uno,200,["Imagenes/enemigos/ENEMY2_%s.PNG"%x for x in range(1,5)],1)
				listaEnemigo.append(enemigo)
				posx += 75
				if x == 9:
					posx = 100

	índiceLance = randint(0,len(listaEnemigo)-1) #índice del enemigo que se va a lanzar a por el jugador
	objetivo_cambio = True
	return índiceLance, objetivo_cambio

# def explotar(x,y,tiempo_inicio,ventana):
# 	#voy a utilizar esta función para mostrar explosiones en los asteroides, después incluso quizá suplante a la actual para los enemigos y la nave del jugador
	
# 	if not time() > tiempo_inicio+2:
# 		ventana.blit(explosion[5], (x,y))

def InvasionEspacial():
	global jej_temporal
	global niv
	global listaEnemigo
	global id_objetivo
	global el_ast

	def generar_asteroides(lista,resolución,cantidad):
		número = 0 #sirve para que no estén todos los asteroides en la misma línea
		for each in range(0,cantidad):
			#Después hacer que tenga en cuenta el tamaño de los asteroides
			x = randint(0,resolución[0])
			lista.append(Asteroide(x,-número))
			número += 20 #resolución[1]/2
		return lista

	tiempo2 = None
	música = []
	for número in range(1,5):
		música.append("./Sonidos/TRACK%s.ogg"%número)
	musc_index = 0 #índice de la pista de música
	sonido = pygame.mixer.Sound(música[musc_index])
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
	
	índiceLance = cargarEnemigos(0)[0]
	#print(timeit(stmt="cargarEnemigos()",number=1,globals=globals()))
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

	#Variables que son usadas en el while principal
	el_ast = 0 #asteroides eliminados,lleva el conteo de asteroides eliminados cuando el nivel es 2
	camp_ast = 1 #campo de asteroides, determina en que nivel va a aparecer el campo de asteroides, VARIABLE TODAVÍA NO IMPLEMENTADA
	gen_ast = True

	tiempo256 = 0
	listaAsteroides = []
	listaExplosiones = []
	acumulador_explosion = 0
	TEMPORAL = True
	potenciador_valor = 0
	tiempo_lance = 5 #Es una variable que determina cada cuanto tiempo un ememigo va a dirigirse hacía el jugador
	#acumulador_lance = 0 Acumulador de lance, representa el valor de X que debe tomar el enemigo cuando se lanza hacía el jugador
	tiene_que_lanzarse = False #esta hace que un enemigo particular se mueva
	tiene_que_lanzarse2 = False #esta habilita al siguiente enemigo a lanzarse
	acumulador_fotograma = 0 #variable que almacena el número de fotograma
	#índiceLance = randint(0,len(listaEnemigo)-1) #índice del enemigo que se va a lanzar a por el jugador
	objetivo_cambio = True #determina si se cambio o no el objetivo de lance
	id_objetivo = id(listaEnemigo[índiceLance])

	while True:
		
		tiempo = (pygame.time.get_ticks()/1000)-tiempo256
		jugador.movimiento()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if (len(listaEnemigo) <= 0 and niv != camp_ast) or (niv == camp_ast and el_ast >= 20):

						#print(timeit(stmt="cargarEnemigos()",number=1,globals=globals()))
						if jugador.eliminado:
							potenciador_valor = 0
						#jugador.tipoDisparo = 0
						tiempo256 = pygame.time.get_ticks()/1000
						jugador.eliminado = False
						jugador.revivir()
						tiempo_lance = tiempo+5
						if jej_temporal:
							niv += 1
						else:
							jej_temporal = True

						if niv < camp_ast:
							índiceLance,objetivo_cambio = cargarEnemigos(0)
						elif niv > camp_ast:
							índiceLance,objetivo_cambio = cargarEnemigos(1)

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
					jugador.disparar(x,y,potenciador_valor)
					
					acumulador = 0
				acumulador += 1

			#problemas acá no entra
			elif bool(keys[K_LEFT]) and bool(keys[K_UP]) and keys[K_SPACE]:
				jugador.rect.left -= jugador.velocidad
				jugador.rect.top -= jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y,potenciador_valor)
					
					acumulador = 0
				acumulador += 1

			elif keys[K_UP] and keys[K_SPACE]:
				jugador.rect.top -= jugador.velocidad
				x,y = jugador.rect.center
				jugador.disparar(x,y,potenciador_valor)
				if acumulador == 10:
					acumulador = 0
				acumulador += 1

			elif keys[K_DOWN] and keys[K_SPACE]:
				jugador.rect.top += jugador.velocidad
				x,y = jugador.rect.center
				jugador.disparar(x,y,potenciador_valor)
				if acumulador == 10:
					acumulador = 0
				acumulador += 1

			elif keys[K_RIGHT] and keys[K_SPACE]:
				jugador.rect.left += jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y,potenciador_valor)
					
					acumulador = 0
				acumulador += 1

			elif keys[K_LEFT] and keys[K_SPACE]:
				jugador.rect.left -= jugador.velocidad
				x,y = jugador.rect.center
				if acumulador == 10:
					jugador.disparar(x,y,potenciador_valor)
					
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
					jugador.disparar(x,y,potenciador_valor)
					
					acumulador = 0
				acumulador += 1
			
		ventana.fill((0,0,0))
		#pygame.draw.rect(ventana, (255,0,0), (resolución[0]/2,resolución[1]/2,4,4))

		#Esto forma parte del muestreo de estrellas
		velocidades = (1,2,3)
		for índice_main,elemento in enumerate(velocidades,0):

			for índice, each in enumerate(listaEstrellas[índice_main],0):
				if each[1] < resolución[1]:
					listaEstrellas[índice_main][índice][1] += elemento
					pygame.draw.rect(ventana, (255,255,255), (each[0],each[1],1,1))
				else:
					pygame.draw.rect(ventana, (255,255,255), (each[0],0,1,1))
					listaEstrellas[índice_main][índice][1] = 0

		#Acá se generan los asteroides
		if len(listaAsteroides) == 0 or (niv == camp_ast and gen_ast):
			if niv != camp_ast:
				listaAsteroides = generar_asteroides(listaAsteroides,resolución,3)
			else:
				listaAsteroides = generar_asteroides(listaAsteroides,resolución,70)
				gen_ast = False
		else:

			#Acá se mueven los asteroides
			for asteroide in listaAsteroides:
				if asteroide.rect.top > resolución[1]:
					listaAsteroides.remove(asteroide)
					if el_ast >= 20:
						pass
					else:
						x = randint(0,resolución[0])
						y = randint(0,resolución[1])
						listaAsteroides.append(Asteroide(x,-y))
				else:
					asteroide.rect.top += asteroide.velocidad
					asteroide.dibujar(ventana)
				if asteroide.rect.colliderect(jugador.rect):
					jugador.destruccion()
					listaAsteroides.remove(asteroide)
					listaEnemigo = []
					jej_temporal = False
					TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
					if jugador.vidas < 1:
						enJuego = False
						detenerTodo()

		if len(listaEnemigo) > 0:
			
			for índice,enemigo in enumerate(listaEnemigo,0):
				# if not "enemigoLance" in locals():
				# 	tiempo2 = enemigo.comportamiento(tiempo,tiempo2,False)
				# else:
				# 	if listaEnemigo[enemigoLance] == enemigo:
				# 		tiempo2 = enemigo.comportamiento(tiempo,tiempo2,True)
				# 	else:
				# 		tiempo2 = enemigo.comportamiento(tiempo,tiempo2,False)
				#print(índice, índiceLance)
				if índice == índiceLance and objetivo_cambio:
					id_objetivo = id(listaEnemigo[índice])
					objetivo_cambio = False

				if id(enemigo) == id_objetivo:
					tiempo2,índiceLance,id_objetivo = enemigo.comportamiento(tiempo,tiempo2,True,índiceLance,jugador,id_objetivo)
					#,tiene_que_lanzarse,tiene_que_lanzarse2,
				else:
					tiempo2,índiceLance,id_objetivo = enemigo.comportamiento(tiempo,tiempo2,False,índiceLance,jugador,id_objetivo) #este último True False todavía no tiene asignado nada, pero va a usarse para determinar el enemigo que se tiene que lanzar
					#,tiene_que_lanzarse,tiene_que_lanzarse2,
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
							jugador.eliminado = True
							listaExplosiones.append((jugador.rect.left,jugador.rect.top,time())) #revisar porque no parece estar funcionando

							enemigo.listadisparo.remove(x)
							listaEnemigo = []
							jej_temporal = False
							TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
							if jugador.vidas < 1:
								print("entro acá")
								enJuego = False
								detenerTodo()
						if x.rect.top > resolución[1]:
							enemigo.listadisparo.remove(x)
			transparencia = 0
				
		else:
			if niv != camp_ast or (niv == camp_ast and el_ast >= 20): #ARREGLAR ESTO
				#print("Entro en este otro lugar")
				tiempo_niv = time() #la hora cuando se muestra el cártel que indica que pasaste de nivel
				if not niv == camp_ast-1:
					TextoNivel = miFuenteNivel.render("Nivel: "+str(niv+1),0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
				else:
					TextoNivel = miFuenteNivel.render("campo de ASTEROIDES",0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")

				if transparencia == 255:
					TEMPORAL = False
				if transparencia < 255 and TEMPORAL:
					transparencia += 5
				else:
					transparencia -= 5
					if transparencia < 0:
						TEMPORAL = True
				TextoNivel.set_alpha(transparencia)
				TextoNivelB.set_alpha(transparencia)

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
							# if enemigo.seLanza:
							# 	índiceLance = randint(0,len(listaEnemigo)-2)
							jugador.listadisparo.remove(x)
							sonidoExplosion.play()
							jugador.puntaje += 100
							TextoPuntaje = miFuente.render("Puntuación: "+str(jugador.puntaje),0,(255,255,255))
							tiempo2 = time()

					for asteroide in listaAsteroides:
						if x.rect.colliderect(asteroide.rect):
							if 0 == randint(0,2):
								potenciador0 = Potenciadores(0,asteroide.rect.left,asteroide.rect.top)
							listaAsteroides.remove(asteroide)
							#acá se genera un error a veces, ni idea porque
							try:
								jugador.listadisparo.remove(x)
							except:
								pass
							#fin de error
							#explotar(asteroide.rect.left,asteroide.rect.top,time(),ventana)
							listaExplosiones.append((asteroide.rect.left,asteroide.rect.top,time())) #pensar si crear una clase para las explosiones o no
							sonidoExplosion.play()
							if niv == camp_ast:
								el_ast += 1
		if not jugador.eliminado:
			jugador.dibujar(ventana)

		if "potenciador0" in globals() or "potenciador0" in locals():
			potenciador0.mover()
			potenciador0.dibujar(ventana)
			if potenciador0.rect.colliderect(jugador):
				#jugador.tipoDisparo = 1
				potenciador_valor = 1
				del potenciador0


		for each in listaExplosiones:
			if (not time() > each[2]+2) and acumulador_explosion < len(explosion):
				ventana.blit(explosion[acumulador_explosion], (each[0],each[1]))
				acumulador_explosion +=1
			else:
				listaExplosiones.remove(each)
				acumulador_explosion = 0
		

		ventana.blit(TextoPuntaje,(30,resolución[1]-30))
		ventana.blit(TextoVidas,(resolución[0]-70,resolución[1]-30))
		
		#función lineal
		# def f(x1,y1,x2,y2,X):
		# 	try:
		# 		m = (y2 - y1)/(x2 - x1)
		# 	except ZeroDivisionError:
		# 		m = 1000
		# 	b = -m*x2+y2
		# 	return round(m*X+b)

		if enJuego == False:
			pygame.mixer.music.fadeout(3000) #se detiene en 3 segundos de forma paulatina
			ventana.blit(gameover,(0,0))
			#ventana.blit(Texto,(resolución[0]/2,resolución[1]/2))
		if acumulador_fotograma % 2 == 0:
			#print(niv)
			if not not not sonido.get_num_channels(): #not not not es más rápido que "not bool()"
				if musc_index < len(música)-1:
					musc_index += 1
				else:
					musc_index = 0
				sonido = pygame.mixer.Sound(música[musc_index])
				sonido.play()
		acumulador_fotograma += 1
		reloj.tick(60)
		pygame.display.update()
		#print(f"{reloj.get_fps():.2f}")

#TEMPORAL = True
InvasionEspacial()

#NOTAS:
#parece haber un problema cuando le disparo al enemigo que se lanza