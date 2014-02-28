# -*- coding: utf-8 -*-

import sys
import copy
import re
import random
import pygame
import time
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
from datetime import datetime
from math import hypot

class City(object):
	def __init__(self,name,x,y):
		self.name=name
		self.x=x
		self.y=y
	
	def __str__(self):
		return "Name = %s, (%f, %f)"%(self.name,self.x,self.y)

class Individual(object):
	def __init__(self,travel):
		self.travel=travel
		self.distance=0.0
		self.evaluate()

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

	def __str__(self):
		return str(self.travel)

	def __repr__(self):
		return "Parcours : " + str(self.travel) + "\nDistance : " + str(self.distance)

	def __len__(self):
		return len(self.travel)

# Test si deux individus sont identiques
def equals(individualA,individualB):
	individualTravelA=individualA.distance
	individualTravelB=individualB.distance
	# for cityA,cityB in zip(individualTravelA,individualTravelB):
		# if cityA!=cityB:
			# return False
	# return True
	return int(individualTravelA)==int(individualTravelB)

# une liste d'objet City
cities=[]
N=2000
population=[]
intermediatePopulation=[]

# GUI
pygame.init()
window=None
screen=None
font=pygame.font.Font(None,30)

def drawText(screen,text,x,y,textColor):
	t=font.render(text,True,textColor)
	textRect=t.get_rect()
	textRect.left=x
	textRect.top=y
	screen.blit(t,textRect)

def drawSolution(screen,citiesIndex):
	colorCircle=(10,10,200)
	radiusCircle=3
	
	screen.fill(0)
	for cityIndex in citiesIndex:
		pygame.draw.circle(screen,colorCircle,(int(cities[cityIndex].x),int(cities[cityIndex].y)),radiusCircle)
		pygame.display.flip()

def drawCities(screen):
	colorCircle=(10,10,200)
	radiusCircle=3
	
	screen.fill(0)
	for city in cities:
		pygame.draw.circle(screen,colorCircle,(city.x,city.y),radiusCircle)
		pygame.display.flip()

def requestCities():
	width=500
	height=500
	window=pygame.display.set_mode((width,height))
	screen=pygame.display.get_surface()
	
	flag=True
	while flag:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_RETURN:
				flag=False
			elif event.type == MOUSEBUTTONDOWN:
				x,y=pygame.mouse.get_pos()
				cities.append(City("v%d"%(len(cities)),x,y))
				drawCities(screen)

def initPopulation():
	# 0 à N
	for i in range(N):
		# On génère la liste des index
		l=list(range(len(cities)))
		# on mélange la liste des index
		random.shuffle(l)
		# on l'ajoute dans la poplulation initiale des individus
		individual=Individual(list(l))
		population.append(individual)
	
	#for individual in population:
	#	print("%s, %f"%(individual.travel,individual.distance))

def select():
	# Tri de la liste, individus ayant la distance la plus courte en premier.
	sorted_pop = sorted(population, key=lambda individual: individual.distance)

	half_point = len(sorted_pop)/2
	curr = 0
	selected_pop = []
#
	while (len(selected_pop) < half_point):
		selected_pop.append(sorted_pop[curr])
		curr = curr + random.randint(1,2)

	# On créé un tableau avec la meilleure moitié de la population
	#selected_pop = sorted_pop[:int(len(sorted_pop)/2)]
	for i in selected_pop:
		intermediatePopulation.append(i)


def cross():
	for individual_index in range(0,len(intermediatePopulation),2):
		crossover(intermediatePopulation[individual_index].travel,intermediatePopulation[individual_index+1].travel)

def crossover(parent1,parent2):
	"""
	Two-point order crossover.
	"""
	crossover_point1 = random.randint(0, len(parent1) - 1)
	crossover_point2 = random.randint(crossover_point1, len(parent1))
	"""
	Get a list of items in parent2, starting from crossover_point2, which
	are not in the middle segment of parent1.
	"""
	unused = [x for x in parent2[crossover_point2:] +
	          parent2[:crossover_point2]
	          if x not in parent1[crossover_point1:crossover_point2]]
	"""
	Copy the middle segment from parent1 to child1, and fill in the empty
	slots from the unused list, beginning with crossover_point2 and
	wrapping around to the beginning.
	"""
	child1 = (unused[len(parent1) - crossover_point2:] +
	          parent1[crossover_point1:crossover_point2] +
	          unused[:len(parent1) - crossover_point2])

	"""
	Get a list of items in parent1, starting from crossover_point2, which
	are not in the middle segment of parent2.
	"""
	unused = [x for x in parent1[crossover_point2:] +
	          parent1[:crossover_point2]
	          if x not in parent2[crossover_point1:crossover_point2]]
	"""
	Copy the middle segment from parent1 to child1, and fill in the empty
	slots from the unused list, beginning with crossover_point2 and
	wrapping around to the beginning.
	"""
	child2 = (unused[len(parent1) - crossover_point2:] +
	          parent2[crossover_point1:crossover_point2] +
	          unused[:len(parent1) - crossover_point2])

	#print("test",crossover_point1,crossover_point2,parent1,parent2,child1,child2)
	intermediatePopulation.append(Individual(child1))
	intermediatePopulation.append(Individual(child2))

# on choisi deux index aléatoires et croise dans la liste les deux villes représenté par les index
def mutate():

	indices = list(range(0,len(intermediatePopulation)))
	random.shuffle(indices)

	for i in indices[:int(len(intermediatePopulation)/100)]:
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
		
		individual.evaluate()
		

def ga_solve(file=None,gui=True,maxtime=0):
	if file==None:
		# afficher l'interface pour récupérer les points (x, y)
		# fonction bloquante
		requestCities()
	else:
		# lecture du fichier
		f=open(file,'r')
		lignes=f.readlines()
		f.close()
		
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
	while True:
		# debug
		# print("Population size = %d"%len(population))
		# print("Intermediate population size = %d"%len(intermediatePopulation))
		# fin debug
		
		select()
		cross()
		mutate()
		
		# print("Population size = %d"%len(population))
		# print("Intermediate population size = %d"%len(intermediatePopulation))
		# gestion du temps
		timespan=datetime.now()-startTime
		if timespan.total_seconds()>maxtime:
			flag=False
			
		for idx,el in enumerate(intermediatePopulation):
			population[idx] = el
		
		del intermediatePopulation[:]

		# recherche du meilleur
		sorted_pop = sorted(population, key=lambda individual: individual.distance)
		elite = sorted_pop[0]
		
		print("elite[0] %s %s"%(str(sorted_pop[0].distance),str(sorted_pop[0].travel)))
		# print("elite[-1] %s",str(sorted_pop[-1].distance))
		
		# print("previousEliteCounter: %d",previousEliteCounter)
		
		# Test si l'élite revient 20x de suite
		if previousElite is not None:
			if equals(elite,previousElite):
				previousEliteCounter+=1
				
				print("Counter: %d", previousEliteCounter)
				if previousEliteCounter>20:
					flag=False
			else:
				previousEliteCounter=0
		
		# time.sleep(1)
		
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
	
	return elite.distance, [cities[i].name for i in elite.travel]

if __name__=="__main__":
	import os
	
	file=None
	gui=True
	maxtime=0
	
	if len(sys.argv)>1:
		if os.path.exists(sys.argv[-1]):
			file=sys.argv[-1]
		if '--nogui' in sys.argv:
			gui=False
		if '--maxtime' in sys.argv:
			index=sys.argv.index('--maxtime')
			if isinstance(int(sys.argv[index+1]),int):
				maxtime=int(sys.argv[index+1])
	else:
		sys.exit("Error : you must provide a list of cities in the parameter\n \
rossier_fort.py <cities file>\n \
Parameters : \n \
	--nogui : start without the GUI\n \
	--maxtime <time in ms>: how long should the algorithm run \n \
")
	try:
		ga_solve(file,gui,maxtime)
	except KeyboardInterrupt:
		try:
			population[0]
			sys.exit("Elite at stop time : ", population[0])
		except:
			sys.exit("Exited")

	
	print("file %s"%file)
	print("gui %d"%gui)
	print("maxtime %d"%maxtime)	