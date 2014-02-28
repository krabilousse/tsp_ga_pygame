# -*- coding: utf-8 -*-

# Développeurs:
# -> Matthieu Rossier, INF3B-DLM
# -> Danick Fort, INF3B-DLM
# ALGORITHME GENETIQUE - Intelligence Artificielle - He-Arc

# version de python utilisé: python 3.3.0

import sys
import copy
import re
import random
import pygame
import time
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
from datetime import datetime
from math import hypot

# Représente une ville, une ville est cractèrisé par
# -> un nom de ville
# -> une position (x, y)
class City(object):
	# Constructeur
	def __init__(self,name,x,y):
		self.name=name
		self.x=x
		self.y=y
	# Permet d'afficher à l'écran une ville
	def __str__(self):
		return "Name = %s, (%f, %f)"%(self.name,self.x,self.y)

# Représente un individu dans une popupalation, un individu est caractérisé par
# -> un "voyage": une liste d'index d'object "City". Les objets "City" sont stocké dans la variable globale "cities"
# -> la distance du voyage
class Individual(object):
	# Constructeur
	def __init__(self,travel):
		self.travel=travel
		self.distance=0.0
		self.evaluate()
	# méthodue qui calcul la distance du "voyage"
	def evaluate(self):
		# distance entre a et b (AB) = sqrt((xb-xa)^2+(yb-ya)^2)
		for i in range(len(cities)-1):
			xa=cities[self.travel[i]].x
			ya=cities[self.travel[i]].y
			xb=cities[self.travel[i+1]].x
			yb=cities[self.travel[i+1]].y
			
			# distance entre deux villes (AB)
			self.distance+=hypot(xb-xa,yb-ya)
		
		# revenir au point de départ à la fin
		xa=cities[self.travel[-1]].x
		ya=cities[self.travel[-1]].y
		xb=cities[self.travel[0]].x
		yb=cities[self.travel[0]].y
		
		self.distance+=hypot(xb-xa,yb-ya)
	# permet d'afficher un "voyage"
	def __str__(self):
		return str(self.travel)
	# permet d'afficher un "voyage"
	def __repr__(self):
		return "Parcours : " + str(self.travel) + "\nDistance : " + str(self.distance)
	# retourne la longueur du "voyage"
	def __len__(self):
		return len(self.travel)

# Test si deux individus (en terme de distance) sont identiques
def equals(individualA,individualB):
	individualDistanceA=individualA.distance
	individualDistanceB=individualB.distance
	return int(individualDistanceA)==int(individualDistanceB)

# une liste d'objet City
cities=[]
# représente la nombre d'individu dans la population
N=2000
# représente la population total
population=[]
# représente la population intermédiaire (après la phase de sélection)
intermediatePopulation=[]

# initialisation de la GUI (pygame)
pygame.init()
# représente la fenêtre (pygame)
window=None
# représenta la zone à dessiner (pygame)
screen=None
# initialiser la possibilité de pouvoir dessiner du texte
font=pygame.font.Font(None,30)

# méthode qui permet de dessiner du texte par rapport à des positions
def drawText(screen,text,x,y,textColor):
	t=font.render(text,True,textColor)
	textRect=t.get_rect()
	textRect.left=x
	textRect.top=y
	screen.blit(t,textRect)

# méthode qui permet de dessiner un voyage d'un individu
# un cercle représente une ville
def drawSolution(screen,citiesIndex):
	colorCircle=(10,10,200)
	radiusCircle=3
	
	screen.fill(0)
	for cityIndex in citiesIndex:
		pygame.draw.circle(screen,colorCircle,(int(cities[cityIndex].x),int(cities[cityIndex].y)),radiusCircle)
		pygame.display.flip()

# méthode qui dessine les villes d'une solution
def drawCities(screen):
	colorCircle=(10,10,200)
	radiusCircle=3
	
	screen.fill(0)
	for city in cities:
		pygame.draw.circle(screen,colorCircle,(city.x,city.y),radiusCircle)
		pygame.display.flip()

# démarre une interface GUI qui demande à l'utilisateur de choisir les positions des villes
def requestCities():
	width=500
	height=500
	window=pygame.display.set_mode((width,height))
	screen=pygame.display.get_surface()
	
	# tant que l'utilisateur ne quitte pas l'interface GUI
	flag=True
	while flag:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_RETURN:
				flag=False
			elif event.type == MOUSEBUTTONDOWN:
				# récupère les positions de la souris
				x,y=pygame.mouse.get_pos()
				# ajoute une ville à la liste globale
				cities.append(City("v%d"%(len(cities)),x,y))
				# on dessine les villes à l'écran
				drawCities(screen)

# première phase de l'AG
# -> on initialise une population aléatoire d'individu
def initPopulation():
	# on vide population
	global population
	population = []
	# 0 à N
	# N => nombre d'individus
	for i in range(N):
		# On génère la liste des index
		l=list(range(len(cities)))
		# on mélange la liste des index
		random.shuffle(l)
		# on l'ajoute dans la poplulation initiale des individus
		individual=Individual(list(l))
		population.append(individual)

# deuxième phase de l'AG
def select():
	# tri de la liste, individus ayant la distance la plus courte en premier.
	sorted_pop = sorted(population, key=lambda individual: individual.distance)

	# la position du milieu de la liste
	half_point = len(sorted_pop)/2
	# représente un index
	curr = 0
	selected_pop = []
	
	# ça sélectionne un individu par rapport à l'index "curr"
	while (len(selected_pop) < half_point):
		selected_pop.append(sorted_pop[curr])
		# on fait varier l'index curr "aléatoirement"
		# ceci est utile pour laisser une chance aux individus "moins bon" ne faisant pas partie de la première partie des meilleurs
		curr = curr + random.randint(1,2)

	# on créé un tableau avec la meilleure moitié de la population
	# selected_pop = sorted_pop[:int(len(sorted_pop)/2)]
	for i in selected_pop:
		intermediatePopulation.append(i)

# troisième phase de l'AG
# l'étape du croisement permet depuis deux parent de donner deux enfants
# nous avois choisi comme algorithme: croisement par des deux points
def cross():
	for individual_index in range(0,len(intermediatePopulation),2):
		crossover(intermediatePopulation[individual_index].travel,intermediatePopulation[individual_index+1].travel)

def crossover(parent1,parent2):
	"""
	croisement sur deux points.
	"""
	#inspiré de https://github.com/mplang/tsp_ga/blob/master/genalg.py
	crossover_point1 = random.randint(0, len(parent1) - 1)
	crossover_point2 = random.randint(crossover_point1, len(parent1))
	"""
	création d'une liste de villes depuis l'individu parent2, commencant à crossover_point2 et finissant à la fin,
	qui n'existent pas dans le segment central de parent1
	"""
	unused = [x for x in parent2[crossover_point2:] +
	          parent2[:crossover_point2]
	          if x not in parent1[crossover_point1:crossover_point2]]
	"""
	copie du segment central de parent1 à child1, et remplir les cases vides
	depuis la liste unused, en commencant par crossover_point2 et en revenant au début
	"""
	child1 = (unused[len(parent1) - crossover_point2:] +
	          parent1[crossover_point1:crossover_point2] +
	          unused[:len(parent1) - crossover_point2])

	"""
	création d'une liste de villes depuis parent1, en commencant à crossover_point2,
	qui ne sont pas dans le segment central de parent2
	"""
	unused = [x for x in parent1[crossover_point2:] +
	          parent1[:crossover_point2]
	          if x not in parent2[crossover_point1:crossover_point2]]
	"""
	copie du segment central de parent1 à child1, et remplir les cases vides
	depuis la liste unused, en commencant à crossover_point2 et en revenant
	au début
	"""
	child2 = (unused[len(parent1) - crossover_point2:] +
	          parent2[crossover_point1:crossover_point2] +
	          unused[:len(parent1) - crossover_point2])

	# copie de child1 et child2 dans la population intermédiaire
	intermediatePopulation.append(Individual(child1))
	intermediatePopulation.append(Individual(child2))

# on choisi deux index aléatoires et croise dans la liste les deux villes représenté par les index
def mutate():
	# mélange des index des individus
	indices = list(range(0,len(intermediatePopulation)))
	random.shuffle(indices)

	# mutation dans 1% des cas
	for i in indices[:int(len(intermediatePopulation)/10)]:
		individual = intermediatePopulation[i]
		# récupération du voyage
		travel=individual.travel
		# index aléatoire 1 (firstIndex)
		firstIndex=random.randint(0,len(travel)-1)
		# index aléatoire 2 (secondIndex)
		secondIndex=random.randint(0,len(travel)-1)
		
		# échange des valeurs par rapport au deux index
		temp=travel[firstIndex]
		travel[firstIndex]=travel[secondIndex]
		travel[secondIndex]=temp
		
		# comme l'individu a été muté, il faut recalculer la distance
		individual.evaluate()
		
# fonction principale du l'algorithme
def ga_solve(file=None,gui=True,maxtime=0):
	# si pas de fichier en entrée
	if file==None:
		# afficher l'interface pour récupérer les points (x, y)
		# fonction bloquante
		requestCities()
	# si on a un fichier text en entrée
	else:
		# lecture du fichier
		f=open(file,'r')
		lignes=f.readlines()
		f.close()
		
		# synthaxe des lignes du fichier
		
		# ville1 x1 y1
		# ville2 x2 y2
		# ...
		for ligne in lignes:
			ligneSplited=ligne.split()
			cities.append(City(ligneSplited[0],float(ligneSplited[1]),float(ligneSplited[2])))
	
	# initialisation de la population initiale
	initPopulation()
	startTime=datetime.now()
	
	# mémorise le meilleur individu précédent
	previousElite=None
	elite = None
	# compteur incrémenté si l'élite revient plusieurs fois de suite
	previousEliteCounter=0
	
	counter=0
	flag=True
	# commence la boucle principale
	# deux conditions de terminaison
	# 1) le temps défini par --maxtime
	# 2) si l'élite revient n fois
	while True:
		# sélection de la population
		select()
		# coisement de la population
		# algorithme croisement sur deux points
		cross()
		# mutation de la population
		# 1% de la population
		mutate()
		
		# timespan représente le durée du temps déjâ passé
		timespan=datetime.now()-startTime
		if timespan.total_seconds()>maxtime:
			flag=False
		
		# copie de l population intermiédiare dans la population total
		for idx,el in enumerate(intermediatePopulation):
			population[idx] = el
		del intermediatePopulation[:]

		# recherche du meilleur
		sorted_pop = sorted(population, key=lambda individual: individual.distance)
		elite = sorted_pop[0]
		
		# Test si l'élite revient 20x de suite
		numberOfApparition=100
		if previousElite is not None:
			# si le elite courant est identique à l'élite précédent
			if equals(elite,previousElite):
				previousEliteCounter+=1
				if previousEliteCounter>numberOfApparition:
					flag=False
			else:
				previousEliteCounter=0
		# mémorisation de l'élite précédent
		previousElite=elite
		
		# afficher le résultat
		if gui:
			path=[]
			for cityIndex in elite.travel:
				path.append((cities[cityIndex].x,cities[cityIndex].y))
				
			if file!=None:
				window=pygame.display.set_mode((500,500))
			
			screen=pygame.display.get_surface()
			screen.fill(0)
			drawSolution(screen,elite.travel)
			pygame.draw.lines(screen,(10,10,200),True,path)
			drawText(screen,str(counter)+" iterations",0,0,(255,255,255))
			drawText(screen,str(timespan),0,30,(255,255,255))
			pygame.display.flip()
		
		counter+=1
	
		if not flag:
			break
	
	# la fonction retourne la liste des noms des ville et "meilleur" distance
	best_travel = [cities[i].name for i in elite.travel]

	del cities[:]
	return elite.distance, best_travel

if __name__=="__main__":
	import os

	instruction_string = "\n \
rossier_fort.py <cities file>\n \
Parameters : \n \
	--nogui : start without the GUI\n \
	--maxtime <time in ms>: how long should the algorithm run \n \
"
	file=None
	gui=True
	maxtime=0
	
	# il au moins > 1 paramètres
	if len(sys.argv)>1:
		# si le dernier paramètre est un nom de fichier valide, alors on le prend comme fichier d'entrée
		if os.path.exists(sys.argv[-1]):
			file=sys.argv[-1]
		# est-ce que l'utilisateur veut une interface GUI qui affiche les résultats
		if '--nogui' in sys.argv:
			gui=False
		# définit le temps maximal que l'algorithme a pour s'exécuter
		if '--maxtime' in sys.argv:
			index=sys.argv.index('--maxtime')
			try:
				if isinstance(int(sys.argv[index+1]),int):
					maxtime=int(sys.argv[index+1])
			except:
				sys.exit("Error : --maxtime <integer> need an integer !" + instruction_string)
	else:
		sys.exit("Error : no parameters provided !" + instruction_string)

	try:
		ga_solve(file,gui,maxtime)
	except KeyboardInterrupt:
		sys.exit("Stopped by user!")
	except:
		raise
		sys.exit("ga_solve raised an exception!")
