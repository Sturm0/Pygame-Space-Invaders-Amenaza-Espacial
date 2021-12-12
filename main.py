import pygame, sys
from pygame.locals import *
from time import sleep, time
from random import randint,uniform,choice
from os import system, name
from random import randint
#from timeit import timeit
#from functools import lru_cache después ver si podes integrar esto en la generación de enemigos
#Actualmente hay dos sistemas de explosiones implementados, uno para los asteroides, nave nodriza, jugador y otro para los enemigos. Mejorar y usar el primero para todo
def limpiar_pantalla():
	if name == "nt":
		system('cls')
	else:
		system('clear')
limpiar_pantalla()
resolución = (1280,720)
with open("Configuraciones.txt",'r') as archivo:
	for each in archivo:
		if each[0] != "#":
			if eval(each.split("=")[1]):
				ventana = pygame.display.set_mode(resolución,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED)
			else:
				ventana = pygame.display.set_mode(resolución)	
pygame.init()

#ventana = pygame.display.set_mode(resolución) #,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED
#Variables globales
jej_temporal = True #Cambiarle el nombre para que se entienda que hace
listaEnemigo = []
explosion = []
id_objetivo = None

niv = 1
#Carga de imagenes
for each in ['./Imagenes/EXPLODE/EXPLODE%s.PNG'%x for x in range(1,21)]:
	if each != None:
		explosion.append(pygame.image.load(each).convert())
listaPotenciadores = [] #imagenes de todos los potenciadores, CAMBIAR EL NOMBRE PARA QUE NO SE CONFUNDA CON lista_potenciadores
for each in ['./Imagenes/Potenciadores/Potenciador_%s.PNG'%x for x in range(0,3)]:
	if each != None:
		listaPotenciadores.append(pygame.image.load(each).convert())

class naveEspacial(pygame.sprite.Sprite):
	#clase para las naves
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load('./Imagenes/SHIP.png').convert()
		self.ImagenExplosion = explosion[0]
		#self.sonidoExplosion = pygame.mixer.Sound()
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = resolución[0]/2
		self.rect.centery = resolución[1]-50
		self.listadisparo = []
		self.vidas = 5
		self.vida = True
		self.eliminado = False
		self.velocidad = 5
		self.puntaje = 0

	def movimiento(self):
		if self.vida == True:
			if self.rect.left <= 0:
				self.rect.left = 0
			elif self.rect.left >= resolución[0]:
				#self.rect.left = resolución[0]
				pass
			if self.rect.top < resolución[1] - resolución[1]/2:
				self.rect.top = resolución[1] - resolución[1]/2
	def disparar(self,x,y,potenciador_valor):
		if potenciador_valor == -1:
			miProyectil = Proyectil(x,y,"Imagenes/SHOTS.png",True)
		elif potenciador_valor == 0:
			miProyectil = Proyectil(x-8,y,"Imagenes/SHOTS2.png",True)
			miProyectil2 = Proyectil(x+5,y,"Imagenes/SHOTS2.png",True)
			self.listadisparo.append(miProyectil2)
		elif potenciador_valor == 1:
			miProyectil = Proyectil(x-8,y,"Imagenes/SHOTS_3.PNG",True)
			for index,each in enumerate([Proyectil(x+5,y,"Imagenes/SHOTS_3.PNG",True),Proyectil(x,y,"Imagenes/SHOTS_3.PNG",True)],0):
				self.listadisparo.append(each)
				if index == 1:
					each.velocidadDisparo -= 1
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
		self.imageProyectil = pygame.image.load(ruta).convert()
		self.rect = self.imageProyectil.get_rect()
		self.rect.top = posy
		self.rect.left = posx
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
		
		self.listaimagenes = [pygame.image.load(each).convert() for each in lista] 

		if tipo == 1:
			self.imagen_disparo = "Imagenes/enemigos/ESHOT_1.png"
		elif tipo == 2:
			pass
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

	def dibujar(self,superficie):
		if self.vida == True:
			self.imagenInvasor = self.listaimagenes[self.posImagen]
		else:
			#acá se muestra la explosión del invasor
			self.imagenInvasor = self.ImagenExplosion[self.posImagen2]
			

		superficie.blit(self.imagenInvasor,self.rect)

	def comportamiento(self,tiempo,tiempo2,seLanza,índiceLance,jugador,id_objetivo,listaExplosiones):
		#algoritmo de comportamiento
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
			#TENGO QUE IMPLEMENTAR ESTA LÓGICA EN EL OTRO SISTEMA DE EXPLOSIONES Y UTILIZAR ESE PARA TODO
			if time() > tiempo2+0.5:
				listaEnemigo.remove(self)
				#self.posImagen2 = 0
				
				if seLanza and len(listaEnemigo) > 0:
					índiceLance = randint(0,len(listaEnemigo)-1)
					id_objetivo = id(listaEnemigo[índiceLance])
			else:
				pass
				# if self.posImagen2 < len(self.ImagenExplosion)-1 and time() >= tiempo2+self.tiempoCambio2:
				# 	self.posImagen2 += 1
				# 	self.tiempoCambio2 += 0.025

		return tiempo2, índiceLance, id_objetivo

			
	def __ataque(self):
		número_random_temporal = randint(1,450)
		if número_random_temporal == self.rangoDisparo:
			self.__disparo()
	def __disparo(self):
		x,y = self.rect.center
		miProyectil = Proyectil(x,y,self.imagen_disparo, False)
		self.listadisparo.append(miProyectil)

	def __movimientos(self):
		self.__movimientoLateral()

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left = self.rect.left + self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False
		else:
			self.rect.left = self.rect.left - self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True

class Nave_nodriza(Invasor):
	def __init__(self,posx,posy,distancia, lista,tipo):
		super().__init__(posx,posy,distancia,lista,tipo)
		#self.vida = None #vida no es usado para nada en nave nodriza porque usa el segundo sistema de explosiones
		self.limiteDerecha = resolución[0] - self.listaimagenes[0].get_size()[0]
		print(self.listaimagenes[0].get_size()[0])
		self.limiteIzquierda = 0
		self.cant_vids = 40
		self.tiempo_rayo_comienzo = 1
		self.laser = pygame.Rect(0,0,0,0)
		self.tiempo_rayo = 0
		self.proyectiles = []
		self.img_orb = pygame.image.load('./Imagenes/enemigos/ORB_0.PNG').convert()

	def comportamiento(self, tiempo,tiempo2, ventana):
		#intentar achicar la funcionalidad de comportamiento de invasor para que pueda ser aprovechada acá más fácilmente
		#self.__movimientos()  
		#self.__movimientoLateral() <- intentar implementar esto bien
		#TODO ESTO ES EQUIVALENTE A __movimientoLateral PERO POR ALGUNA RAZÓN TIRA ERROR CUANDO LO INTENTO USAR
		if self.derecha == True:
			self.rect.left = self.rect.left + self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False
		else:
			self.rect.left = self.rect.left - self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True

		if self.tiempoCambio == round(tiempo):
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaimagenes)-1:
				self.posImagen = 0

		if self.tiempo_rayo_comienzo == round(tiempo):
			self.tiempo_rayo_comienzo += 3
			self.tiempo_rayo = round(tiempo)

			for each in range(3):
				self.proyectiles.append(self.img_orb.get_rect(topleft=(self.rect.midbottom[0],self.rect.midbottom[1])))
				

		if tiempo > self.tiempo_rayo and tiempo < self.tiempo_rayo+1:
			self.__disparo(ventana)

		try:
			if self.proyectiles[0].top < resolución[1]:
				self.proyectiles[0].top += 5

			if self.proyectiles[1].top < resolución[1]:
				self.proyectiles[1].top += 5
				self.proyectiles[1].left -= 4

			if self.proyectiles[2].top < resolución[1]:
				self.proyectiles[2].top += 5
				self.proyectiles[2].left += 4

			for each in self.proyectiles:
				ventana.blit(self.img_orb,each)

				if each.top > resolución[1]:
					
					self.proyectiles = []

		except:
			pass

		return tiempo2

	def __ataque(self,ventana):
		pass

	def __disparo(self,ventana):
		self.laser = pygame.Rect(self.rect.midbottom[0],self.rect.midbottom[1],8, resolución[1])
		pygame.draw.rect(ventana,(135,206,235),self.laser)
		#return tiempo2
		
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
				listaEnemigo.append(enemigo)
				posx += 75
				if x == 9:
					posx = 100
	else:
		for cada_uno in lista_y:
			for x in range(1,10):
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
	#nuev_niv = [False,0]

	#Generación de estrellas
	listaEstrellas = [[],[],[]]
	for cada_elemento in range(0,3):
		for each in range(1,41):
			x_aleatorio = randint(0,resolución[0])
			y_aleatorio = randint(0,resolución[1])
			listaEstrellas[cada_elemento].append([x_aleatorio,y_aleatorio])

	#Variables que son usadas en el while principal
	el_ast = 0 #asteroides eliminados,lleva el conteo de asteroides eliminados cuando el nivel es 2
	camp_ast = 10 #campo de asteroides, determina en que nivel va a aparecer el campo de asteroides
	gen_ast = True
	niv_nod = 15 #nivel en el que aparece la nave nodriza, en el juego original es en el nivel 15

	lista_potenciadores = [] #esta lista contiene todos los potenciadores que se muestran en la ventana 
	tiempo256 = 0
	listaAsteroides = []
	listaExplosiones = []
	acumulador_explosion = 0
	TEMPORAL = True
	potenciador_valor = -1
	tiempo_lance = 5 #Es una variable que determina cada cuanto tiempo un ememigo va a dirigirse hacía el jugador
	#acumulador_lance = 0 Acumulador de lance, representa el valor de X que debe tomar el enemigo cuando se lanza hacía el jugador
	tiene_que_lanzarse = False #esta hace que un enemigo particular se mueva
	tiene_que_lanzarse2 = False #esta habilita al siguiente enemigo a lanzarse
	acumulador_fotograma = 0 #variable que almacena el número de fotograma
	#índiceLance = randint(0,len(listaEnemigo)-1) #índice del enemigo que se va a lanzar a por el jugador
	objetivo_cambio = True #determina si se cambio o no el objetivo de lance
	id_objetivo = id(listaEnemigo[índiceLance])


	#función para la muerte del jugador cuando lo mata la nave nodriza, la idea es después mejorarla para que incluya cualquier tipo de muerte del jugador
	def morir_nod(nave_nodriza0,jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego):
		#del nave_nodriza0 #por alguna razón no se puede eliminar nave_nodriza0 desde acá, ni idea
		jugador.destruccion()
		jugador.eliminado = True
		listaExplosiones.append((jugador.rect.left,jugador.rect.top,time()))
		listaEnemigo = []
		jej_temporal = False
		TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
		if jugador.vidas < 1:
			enJuego = False
			detenerTodo()
		return listaEnemigo, jej_temporal, TextoVidas, enJuego
		
	while True:
		
		tiempo = (pygame.time.get_ticks()/1000)-tiempo256
		jugador.movimiento()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if (len(listaEnemigo) <= 0 and niv != camp_ast) or (niv == camp_ast):

						#print(timeit(stmt="cargarEnemigos()",number=1,globals=globals()))
						if jugador.eliminado:
							potenciador_valor = -1
						tiempo256 = pygame.time.get_ticks()/1000
						jugador.eliminado = False
						jugador.revivir()
						tiempo_lance = tiempo+5
						if jej_temporal: #jej_temporal parece evitar que pase de nivel cuando el jugador es eliminado
							niv += 1
						else:
							jej_temporal = True

						if niv < camp_ast:
							índiceLance,objetivo_cambio = cargarEnemigos(0)

						elif niv == niv_nod:
							nave_nodriza0 = Nave_nodriza(resolución[0]/2,20,7000,["./Imagenes/enemigos/BOSS_%s.png"%x for x in range(0,3)],2) #el 7000 no debería tener ningún efecto

							print(nave_nodriza0.limiteDerecha)
							print(nave_nodriza0.limiteIzquierda)

						elif niv > camp_ast:
							índiceLance,objetivo_cambio = cargarEnemigos(1)
						

		#Acá se configura la asignación de teclas
		keys = pygame.key.get_pressed()

		if enJuego == True and 1 in keys:

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
				if asteroide.rect.colliderect(jugador.rect) and not jugador.eliminado:
					
					#ESTA SECCIÓN DE ACÁ ES IGUAL A UNA MÁS ABAJO
					listaAsteroides.remove(asteroide)
					jugador.destruccion()
					jugador.eliminado = True
					listaExplosiones.append((jugador.rect.left,jugador.rect.top,time()))
					listaEnemigo = []
					jej_temporal = False
					TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
					el_ast = 0 
					if jugador.vidas < 1:
						print("entro acá")
						enJuego = False
						detenerTodo()



		if "nave_nodriza0" in locals() or "nave_nodriza0" in globals():
			nave_nodriza0.dibujar(ventana)
			tiempo2 = nave_nodriza0.comportamiento(tiempo,tiempo2,ventana)
			if nave_nodriza0.laser.colliderect(jugador.rect):
				listaEnemigo, jej_temporal, TextoVidas, enJuego = morir_nod(nave_nodriza0,jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego)
				del nave_nodriza0
			else:
				if jugador.rect.collidelist(nave_nodriza0.proyectiles) > -1:
					listaEnemigo, jej_temporal, TextoVidas, enJuego = morir_nod(nave_nodriza0,jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego)
					del nave_nodriza0


		if len(listaEnemigo) > 0:
			
			for índice,enemigo in enumerate(listaEnemigo,0):

				if índice == índiceLance and objetivo_cambio:
					id_objetivo = id(listaEnemigo[índice])
					objetivo_cambio = False

				if id(enemigo) == id_objetivo:
					tiempo2,índiceLance,id_objetivo = enemigo.comportamiento(tiempo,tiempo2,True,índiceLance,jugador,id_objetivo,listaExplosiones)
				else:
					tiempo2,índiceLance,id_objetivo = enemigo.comportamiento(tiempo,tiempo2,False,índiceLance,jugador,id_objetivo,listaExplosiones)
					
				enemigo.dibujar(ventana)

				if enemigo.rect.colliderect(jugador.rect):
					print("entro acá")
					#Y A SU VEZ ESTA ES IGUAL A OTRA MÁS ABAJO, JEJ
					listaEnemigo.remove(enemigo)
					jugador.destruccion()
					jugador.eliminado = True
					listaExplosiones.append((jugador.rect.left,jugador.rect.top,time()))
					listaEnemigo = []
					jej_temporal = False
					TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
					if jugador.vidas < 1:
						print("entro acá")
						enJuego = False
						detenerTodo()

				if len(enemigo.listadisparo) > 0:

					for x in enemigo.listadisparo:
						
						x.dibujar(ventana)
						x.trayectoria()
						if x.rect.colliderect(jugador.rect):

							#LA LÍNEA 589 HACE REFERENCIA A LO QUE VIENE A CONTINUACIÓN:
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
			if (niv != camp_ast or el_ast >= 20 or jugador.eliminado) and (niv != niv_nod or ("nave_nodriza0" not in locals() and "nave_nodriza0" not in globals())):
				tiempo_niv = time() #la hora cuando se muestra el cártel que indica que pasaste de nivel
				if (niv == camp_ast-1 and not jugador.eliminado) or (niv == camp_ast and jugador.eliminado):
					TextoNivel = miFuenteNivel.render("campo de ASTEROIDES",0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")

				elif (niv == niv_nod-1 and not jugador.eliminado) or (niv == niv_nod and jugador.eliminado):
					TextoNivel = miFuenteNivel.render("NAVE NODRIZA",0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")

				elif not jugador.eliminado:
					TextoNivel = miFuenteNivel.render("Nivel: "+str(niv+1),0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
				else:
					TextoNivel = miFuenteNivel.render("Nivel: "+str(niv),0,(255,255,255))
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

							jugador.listadisparo.remove(x)
							listaExplosiones.append((enemigo.rect.left,enemigo.rect.top,time()))
							del enemigo
							sonidoExplosion.play()
							jugador.puntaje += 100
							TextoPuntaje = miFuente.render("Puntuación: "+str(jugador.puntaje),0,(255,255,255))
							tiempo2 = time()

					for asteroide in listaAsteroides:
						if x.rect.colliderect(asteroide.rect):
							if randint(0,100) <= 40: 
								lista_potenciadores.append(Potenciadores(0,asteroide.rect.left,asteroide.rect.top))
							elif randint(0,100) <= 30:
								lista_potenciadores.append(Potenciadores(1,asteroide.rect.left,asteroide.rect.top))
							elif randint(0,100) <= 20:
								lista_potenciadores.append(Potenciadores(1,asteroide.rect.left,asteroide.rect.top))
							elif randint(0,100) <= 18:
								lista_potenciadores.append(Potenciadores(2,asteroide.rect.left,asteroide.rect.top))
								
							listaAsteroides.remove(asteroide)
							#acá se genera un error a veces, ni idea porque
							try:
								jugador.listadisparo.remove(x)
							except:
								pass
							listaExplosiones.append((asteroide.rect.left,asteroide.rect.top,time()))
							sonidoExplosion.play()
							if niv == camp_ast:
								el_ast += 1
								if el_ast >= 20:
									jugador.rect.left += resolución[0]+1000

					if niv == niv_nod and ("nave_nodriza0" in locals() or "nave_nodriza0" in globals()):
						if x.rect.colliderect(nave_nodriza0):
							#es muy similar a lo de la línea 675, separar en una función
							#nave_nodriza0.vida = False

							listaExplosiones.append((x.rect.left,x.rect.top,time()))
							jugador.listadisparo.remove(x)
							sonidoExplosion.play()
							
							TextoPuntaje = miFuente.render("Puntuación: "+str(jugador.puntaje),0,(255,255,255))
							tiempo2 = time()
							nave_nodriza0.cant_vids -= 1
							print(nave_nodriza0.cant_vids)

							if nave_nodriza0.cant_vids <= 0:
								
								jugador.puntaje += 1000
								listaExplosiones.append((nave_nodriza0.rect.left,nave_nodriza0.rect.top,time()))
								del nave_nodriza0
									
		if not jugador.eliminado:
			jugador.dibujar(ventana)

		for each in lista_potenciadores:
			each.mover()
			each.dibujar(ventana)
			if each.rect.colliderect(jugador):
				if each.tipo == 0:
					potenciador_valor = 0
				elif each.tipo == 1:
					potenciador_valor = 1
				elif each.tipo == 2:
					jugador.vidas += 1
					TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
				lista_potenciadores.remove(each)
				
		tiempo_cambio_temp = 0.025
		for each in listaExplosiones:
			if acumulador_explosion < len(explosion):
				ventana.blit(explosion[acumulador_explosion], (each[0],each[1]))
				if time() >= each[2]+tiempo_cambio_temp:
					acumulador_explosion +=1
					tiempo_cambio_temp += 0.025
			else:
				listaExplosiones.remove(each)
				acumulador_explosion = 0
		

		ventana.blit(TextoPuntaje,(30,resolución[1]-30))
		ventana.blit(TextoVidas,(resolución[0]-70,resolución[1]-30))
		
		if enJuego == False:
			pygame.mixer.music.fadeout(3000) #se detiene en 3 segundos de forma paulatina
			ventana.blit(gameover,(0,0))

		if acumulador_fotograma % 2 == 0:
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


InvasionEspacial()