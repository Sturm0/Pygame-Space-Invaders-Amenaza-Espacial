import pygame
from random import randint
from time import time
from Explosion import Explosion

class Asteroide():
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
		
	def recibir_disparo(self,niv,camp_ast,lista_potenciadores,listaAsteroides,listadisparo,listaExplosiones,el_ast,listaPotenciadores,sonidoExplosion,sonido_potenciadores):
		from Potenciadores import Potenciadores
		
		if niv == camp_ast:
			prob_poten = 20 # es para que no aparezcan demasiados potenciadores en el nivel del campo de asteroides
		else:
			prob_poten = 40
		if randint(0,100) <= prob_poten:
			lista_potenciadores.append(Potenciadores(0,self.rect.left,self.rect.top,listaPotenciadores,sonido_potenciadores))
		elif randint(0,100) <= prob_poten-10:
			lista_potenciadores.append(Potenciadores(1,self.rect.left,self.rect.top,listaPotenciadores,sonido_potenciadores))
		elif randint(0,100) <= prob_poten-20:
			lista_potenciadores.append(Potenciadores(2,self.rect.left,self.rect.top,listaPotenciadores,sonido_potenciadores))
			
		listaAsteroides.remove(self)
		#acá se genera un error a veces, ni idea porque
		try:
			listadisparo.remove(x)
		except:
			pass
		listaExplosiones.append([self.rect.left,self.rect.top,time(),0])
		una_explosion = Explosion(sonidoExplosion)
		una_explosion.sonidoExplosion.play()
		if niv == camp_ast:
			el_ast += 1
		return el_ast
