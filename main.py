import pygame, sys
from pygame.locals import *
from time import sleep, time
from random import randint,uniform,choice
from os import system, name
from random import randint
from naveEspacial import *
from Proyectil import *
from Invasor import *
from Nave_nodriza import *
from Asteroide import *
from Potenciadores import *
from Explosion import *
from pathlib import Path
#from timeit import timeit
#from functools import lru_cache después ver si podes integrar esto en la generación de enemigos
#Actualmente hay dos sistemas de explosiones implementados, uno para los asteroides, nave nodriza, jugador y otro para los enemigos. Mejorar y usar el primero para todo
def limpiar_pantalla():
	if name == "nt":
		system('cls')
	else:
		system('clear')
limpiar_pantalla()
resolución = (800,600)

with open(Path(__file__).parent/"Configuraciones.txt",'r') as archivo:
	for each in archivo:
		if each[0] != "#":
			if eval(each.split("=")[1]):
				ventana = pygame.display.set_mode(resolución,flags=pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED)
			else:
				ventana = pygame.display.set_mode(resolución)	
pygame.init()
pygame.display.set_caption("Space Invaders Amenaza Espacial")

#Variables globales
jej_temporal = True #Cambiarle el nombre para que se entienda que hace
listaEnemigo = []
id_objetivo = None
explosion = []

niv = 0
#Carga de imagenes
logo = pygame.image.load(Path(__file__).parent/"Imagenes/LOGO.png").convert()
size_logo = logo.get_size()
vent_rect = ventana.get_rect()
logo_rect = logo.get_rect()
logo_rect.center = vent_rect.center

EXPLOSION_IMAGEN = pygame.image.load(Path(__file__).parent/'Imagenes/EXPLODE.PNG').convert()
imagenes_invasores_todo_unido = [pygame.image.load(Path(__file__).parent/'Imagenes/enemigos/ENEMY.PNG').convert()
					            ,pygame.image.load(Path(__file__).parent/'Imagenes/enemigos/ENEMY2.PNG').convert()
					            ,pygame.image.load(Path(__file__).parent/'Imagenes/enemigos/ENEMY3.PNG').convert()]
					 
imagen_potenciadores_todo_unido = pygame.image.load(Path(__file__).parent/'Imagenes/POWERUPS.PNG').convert()
imagen_asteroides_todo_unido = pygame.image.load(Path(__file__).parent/'Imagenes/ASTEROIDS.PNG').convert()
imagen_nave_nodriza_todo_unido = pygame.image.load(Path(__file__).parent/'Imagenes/enemigos/BOSS.PNG').convert()

imagen_disparos_invasor = pygame.image.load(Path(__file__).parent/'Imagenes/enemigos/ESHOTS.PNG').convert()
disparos_jugador = [pygame.image.load(each).convert() for each in [Path(__file__).parent/"Imagenes/SHOTS.png",Path(__file__).parent/"Imagenes/SHOTS2.png",Path(__file__).parent/"Imagenes/SHOTS3.png"]]

def partidor_de_imagenes(ancho_de_sprite,imagen):
	#esta función es para obtener cada uno de los sprites de por ejemplo la tira de sprites que es ASTEROIDS.PNG
	sprite_inicio = 0 #indica cuantos pixeles a la izquierda está el origen en la imagen, para poder ir seleccionando los distintos estados del sprite
	res = []
	while sprite_inicio < imagen.get_width():
		superficie = pygame.Surface((ancho_de_sprite, imagen.get_height()))
		superficie.blit(imagen,(0,0),(sprite_inicio,0,ancho_de_sprite,imagen.get_height()))
		res.append(superficie)
		sprite_inicio += ancho_de_sprite
	return res
	
#acá se parten las imagenes anteriormente cargadas
imagenes_explosion = partidor_de_imagenes(32,EXPLOSION_IMAGEN)
imagenes_invasores = [partidor_de_imagenes(32,imagenes_invasores_todo_unido[i]) for i in range(len(imagenes_invasores_todo_unido))]
imagenes_potenciadores = partidor_de_imagenes(32,imagen_potenciadores_todo_unido)
del imagenes_potenciadores[2] #porque la verdad que no tengo idea que hace ese potenciador
imagenes_asteroides = partidor_de_imagenes(32,imagen_asteroides_todo_unido)
imagenes_nave_nodriza = partidor_de_imagenes(96,imagen_nave_nodriza_todo_unido)
disparos_invasor = partidor_de_imagenes(7,imagen_disparos_invasor)
#Carga de sonido
pygame.mixer.set_num_channels(20) #porque si no hay muchos sonidos que no se escuchan
sonido_potenciadores = pygame.mixer.Sound(Path(__file__).parent/'Sonidos/POWER.WAV')

def detenerTodo(*args):
	for enemigo in listaEnemigo:
		for disparo in enemigo.listadisparo:
			enemigo.listadisparo.remove(disparo)
		enemigo.conquista = True
		
#se podría agregar un decorador cache a esta función para hacerla más rápida
#@lru_cache(maxsize=2)
#							|-mejorar esto-|
posición_limite = resolución[0]-((resolución[0]*(1/2))/9)*8-32
valor_aum = (resolución[0]*(1/2))/9
def cargarEnemigos(tipo):
	lista_y = [20,120,220]
	posx = 0
	#todas esta sección debería estar ligada a la resolución o van a surgir problemas al cambiarse la resolución
	for cada_uno in lista_y:
			for x in range(1,11):
				enemigo = Invasor(posx,cada_uno,posición_limite,imagenes_invasores,disparos_invasor,tipo,resolución)
				listaEnemigo.append(enemigo)
				posx += valor_aum
				if x == 9:
					posx = 0

	índiceLance = randint(0,len(listaEnemigo)-1) #índice del enemigo que se va a lanzar a por el jugador
	objetivo_cambio = True
	return índiceLance, objetivo_cambio

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
			lista.append(Asteroide(x,-número,imagenes_asteroides))
			número += 20 #resolución[1]/2
		return lista

	tiempo2 = None
	música = []
	for número in range(1,5):
		música.append(Path(__file__).parent/("Sonidos/TRACK%s.ogg"%número))
	musc_index = 0 #índice de la pista de música
	sonido = pygame.mixer.Sound(música[musc_index])
	sonidoExplosion = pygame.mixer.Sound(Path(__file__).parent/'Sonidos/EXPLODE.WAV')
	
	sonido.play()
	gameover = pygame.image.load(Path(__file__).parent/'Imagenes/gameover.bmp').convert()
	gameover = pygame.transform.scale(gameover,(resolución[0],resolución[1]))

	#Fuentes
	miFuente = pygame.font.Font(None,20)
	miFuenteFin = pygame.font.Font(None,90)
	miFuenteNivel = pygame.font.Font(None,50)
	Texto = miFuenteFin.render("Fin del juego",0,(120,100,40))

	jugador = naveEspacial(imagenes_explosion,resolución,disparos_jugador)
	TextoPuntaje = miFuente.render("Puntuación: "+str(jugador.puntaje),0,(255,255,255))
	TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
	
	#print(timeit(stmt="cargarEnemigos()",number=1,globals=globals()))
	enJuego = True
	tiempo_niv = 0
	reloj = pygame.time.Clock()

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
	tiempo_lance = 5 #Es una variable que determina cada cuanto tiempo un ememigo va a dirigirse hacía el jugador
	#acumulador_lance = 0 Acumulador de lance, representa el valor de X que debe tomar el enemigo cuando se lanza hacía el jugador
	tiene_que_lanzarse = False #esta hace que un enemigo particular se mueva
	tiene_que_lanzarse2 = False #esta habilita al siguiente enemigo a lanzarse
	acumulador_fotograma = 0 #variable que almacena el número de fotograma
	#índiceLance = randint(0,len(listaEnemigo)-1) #índice del enemigo que se va a lanzar a por el jugador
	objetivo_cambio = True #determina si se cambio o no el objetivo de lance
	prob_poten = 40 #determina la probabilidad de que aparezca un potenciador
	#id_objetivo = id(listaEnemigo[índiceLance])
	nave_nodriza0 = None


	#función para la muerte del jugador cuando lo mata la nave nodriza, la idea es después mejorarla para que incluya cualquier tipo de muerte del jugador
	def morir_jugador(jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego,listaAsteroides=None,asteroide=None,nave_nodriza0=False):
		#del nave_nodriza0 #por alguna razón no se puede eliminar nave_nodriza0 desde acá, ni idea
	
		jugador.destruccion()
		jugador.eliminado = True
		Explosion(jugador.rect.left,jugador.rect.top,sonidoExplosion,imagenes_explosion,listaExplosiones)
		listaEnemigo = []
		jej_temporal = False
		TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
		if jugador.vidas < 1:
			enJuego = False
			detenerTodo()

		if type(listaAsteroides) == list:
			listaAsteroides.remove(asteroide)
			el_ast = 0
			return listaEnemigo, jej_temporal, TextoVidas, enJuego, el_ast
		else:
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
							jugador.potenciador_val = -1
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
							nave_nodriza0 = Nave_nodriza(resolución[0]/2,20,resolución,imagenes_nave_nodriza)
							

						elif niv > camp_ast and niv < niv_nod+2:
							índiceLance,objetivo_cambio = cargarEnemigos(1)

						elif niv >= niv_nod+2:
							índiceLance,objetivo_cambio = cargarEnemigos(2)
					elif niv == 0:
						índiceLance = cargarEnemigos(0)[0]
				elif event.key == pygame.K_ESCAPE:						
					pygame.quit()
					sys.exit()
		#Acá se configura la asignación de teclas
		keys = pygame.key.get_pressed()

		if enJuego == True and 1 in keys:
			jugador.entrada(keys) #esto revisa la entrada del jugador y se encarga de mover y disparar acorde
			
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
						listaAsteroides.append(Asteroide(x,-y,imagenes_asteroides))
				else:
					asteroide.rect.top += asteroide.velocidad
					if asteroide.rect.top > 0:
						asteroide.dibujar(ventana)
				if asteroide.rect.colliderect(jugador.rect) and not jugador.eliminado:
					
					listaEnemigo, jej_temporal, TextoVidas, enJuego, el_ast = morir_jugador(jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego,listaAsteroides,asteroide)

		if nave_nodriza0 != None:
			nave_nodriza0.dibujar(ventana)
			tiempo2 = nave_nodriza0.comportamiento(tiempo,tiempo2,ventana)
			if nave_nodriza0.laser.colliderect(jugador.rect):
				listaEnemigo, jej_temporal, TextoVidas, enJuego = morir_jugador(jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego,None,None,nave_nodriza0)
				nave_nodriza0 = None
			else:
				if jugador.rect.collidelist(nave_nodriza0.lista_orbes) > -1:
					listaEnemigo, jej_temporal, TextoVidas, enJuego = morir_jugador(jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego,None,None,nave_nodriza0)
					nave_nodriza0 = None


		if len(listaEnemigo) > 0 and niv != 0:
			
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
					listaEnemigo, jej_temporal, TextoVidas, enJuego = morir_jugador(jugador,listaExplosiones,listaEnemigo,jej_temporal,TextoVidas,enJuego)

				if len(enemigo.listadisparo) > 0:

					for x in enemigo.listadisparo:
						
						x.dibujar(ventana)
						x.trayectoria()
						if x.rect.colliderect(jugador.rect):

							#LA LÍNEA 589 HACE REFERENCIA A LO QUE VIENE A CONTINUACIÓN:
							jugador.destruccion()
							jugador.eliminado = True
							Explosion(jugador.rect.left,jugador.rect.top,sonidoExplosion,imagenes_explosion,listaExplosiones)

							enemigo.listadisparo.remove(x)
							listaEnemigo = []
							jej_temporal = False
							TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
							if jugador.vidas < 1:
								enJuego = False
								detenerTodo()
						if x.rect.top > resolución[1]:
							enemigo.listadisparo.remove(x)
			transparencia = 0
				
		elif niv != 0:
			# ~ transparencia = 0 #ELIMINAR ESTO UNA VEZ QUE TERMINES DE DEPURAR!
			if (niv != camp_ast or el_ast >= 20 or jugador.eliminado) and (niv != niv_nod or nave_nodriza0 == None):
				tiempo_niv = time() #la hora cuando se muestra el cártel que indica que pasaste de nivel
				if (niv == camp_ast-1 and not jugador.eliminado) or (niv == camp_ast and jugador.eliminado):
					TextoNivel = miFuenteNivel.render("campo de ASTEROIDES",0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
					jugador.rect.left += resolución[0]+1000

				elif (niv == niv_nod-1 and not jugador.eliminado) or (niv == niv_nod and jugador.eliminado):
					TextoNivel = miFuenteNivel.render("NAVE NODRIZA",0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
					jugador.rect.left += resolución[0]+1000

				elif not jugador.eliminado:
					TextoNivel = miFuenteNivel.render("Nivel: "+str(niv+1),0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
					jugador.rect.left += resolución[0]+1000
				else:
					TextoNivel = miFuenteNivel.render("Nivel: "+str(niv),0,(255,255,255))
					TextoNivelB = miFuenteNivel.render("pulsa INTRO para seguir",0,(255,255,255))
					tamaño_texto = miFuenteNivel.size("pulsa INTRO para seguir")
					jugador.rect.left += resolución[0]+1000

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

				if x.rect.top < 0: #para que se eliminen las balas cuando no están en la ventana
					jugador.listadisparo.remove(x)
				else:
					for enemigo in listaEnemigo:
						if x.rect.colliderect(enemigo.rect):
							
							TextoPuntaje = enemigo.recibir_disparo(listaEnemigo,sonidoExplosion,imagenes_explosion,listaExplosiones,jugador,x,miFuente)
							tiempo2 = time()
							
							if enemigo.seLanza and len(listaEnemigo) > 0:
								índiceLance = randint(0,len(listaEnemigo)-1)
								id_objetivo = id(listaEnemigo[índiceLance])

					for asteroide in listaAsteroides:
						if x.rect.colliderect(asteroide.rect):
							el_ast = asteroide.recibir_disparo(niv,camp_ast,lista_potenciadores,listaAsteroides,jugador.listadisparo,listaExplosiones,el_ast,imagenes_potenciadores,sonidoExplosion,sonido_potenciadores,imagenes_explosion)

					if niv == niv_nod and nave_nodriza0 != None:
						if x.rect.colliderect(nave_nodriza0):
							TextoPuntaje, nave_nodriza0 = nave_nodriza0.recibir_disparo(sonidoExplosion,imagenes_explosion,listaExplosiones,jugador,x,miFuente)
							tiempo2 = time()
						if nave_nodriza0 != None and x.rect.collidelist(nave_nodriza0.lista_orbes) != -1:
							nave_nodriza0.lista_orbes[x.rect.collidelist(nave_nodriza0.lista_orbes)].recibir_disparo(jugador, x)
									
		if not jugador.eliminado and jugador.rect.left < resolución[0]: #jugador.rect.top < resolucion[1]
			jugador.dibujar(ventana)

		for each in lista_potenciadores:
			each.mover()
			each.dibujar(ventana)
			if each.rect.colliderect(jugador):
				pygame.mixer.Channel(7).play(each.sonido) #sin esto de channel 7 el sonido del potenciador no puede reproducirse a la vez que otros sonidos, más info en el commit
				
				if each.tipo == 0:
					jugador.potenciador_val = 0
				elif each.tipo == 1:
					jugador.potenciador_val = 1
				elif each.tipo == 2:
					jugador.vidas += 1
					TextoVidas = miFuente.render("Vidas: "+str(jugador.vidas),0,(255,255,255))
				lista_potenciadores.remove(each)
				
		for each in listaExplosiones:
			each.comportamiento(tiempo,listaExplosiones)
			each.dibujar(ventana)

		ventana.blit(TextoPuntaje,(30,resolución[1]-30))
		ventana.blit(TextoVidas,(resolución[0]-70,resolución[1]-30))
		
		if enJuego == False:
			pygame.mixer.music.fadeout(3000) #se detiene en 3 segundos de forma paulatina
			ventana.blit(gameover,(0,0))

		if acumulador_fotograma % 2 == 0:
			#print(f"{reloj.get_fps():.2f}")
			if not not not sonido.get_num_channels(): #not not not es más rápido que "not bool()"
				if musc_index < len(música)-1:
					musc_index += 1
				else:
					musc_index = 0

				sonido = pygame.mixer.Sound(música[musc_index])
				sonido.play()

		if niv == 0:
			ventana.blit(logo,(logo_rect))
			jugador.rect.left = resolución[0]+700
		acumulador_fotograma += 1
		reloj.tick(60)
		pygame.display.update()

InvasionEspacial()
