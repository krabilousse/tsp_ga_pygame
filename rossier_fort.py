# -*- coding: utf-8 -*-

import sys
import re
import random
import datetime

from math import sqrt, pow

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
	
	def evaluate(self):
		# distance entre a et b (AB) = sqrt((xb-xa)^2+(yb-ya)^2)
		for i in range(len(cities)-1):
			xa=cities[self.travel[i]].x
			ya=cities[self.travel[i]].y
			xb=cities[self.travel[i+1]].x
			yb=cities[self.travel[i+1]].y
			
			# distance entre deux villes (AB)
			self.distance+=sqrt(pow(xb-xa,2)+pow(yb-ya,2))
		
		# revenir au point de départ à la fin
		xa=cities[self.travel[-1]].x
		ya=cities[self.travel[-1]].y
		xb=cities[self.travel[0]].x
		yb=cities[self.travel[0]].y
		
		self.distance+=sqrt(pow(xb-xa,2)+pow(yb-ya,2))

# une liste d'objet City
cities=[]

N=1024
population=[]
intermediatePopulation=[]

def initPopulation():
	# 0 à N
	for i in range(N):
		# On génère la liste des index
		l=list(range(len(cities)))
		# on mélange la liste des index
		random.shuffle(l)
		# on l'ajoute dans la poplulation initiale des individus
		individual=Individual(list(l))
		individual.evaluate()
		population.append(individual)
	
	for individual in population:
		print("%s, %f"%(individual.travel,individual.distance))
		

#def evaluate(individual):
#	pass

def select():
	# Tri de la liste, individus ayant la distance la plus courte en premier.
	sorted_pop = sorted(population, key=lambda individual: individual.distance)
	#for i in sorted_pop:
	#	print(i.distance)
	# On créé un tableau avec la meilleure moitié de la population
	besthalf_pop = sorted_pop[len(sorted_pop)/2:]
	intermediatePopulation = besthalf_pop

def cross():
	for i in range(0,len(intermediatePopulation)-2):
		

# on choisi deux index aléatoires et croise dans la liste les deux villes représenté par les index
def mutate():
	for individual in intermediatePopulation:
		# récupération du voyage
		travel=individual.travel
		# index aléatoire 1 (firstIndex)
		firstIndex=random.randint(0,len(travel))
		# index aléatoire 2 (secondIndex)
		secondIndex=random.randint(0,len(travel))
		
		# échange des valeurs par rapport au deux index
		temp=travel[firstIndex]
		travel[firstIndex]=travel[secondIndex]
		travel[secondIndex]=temp
		

def ga_solve(file=None,gui=True,maxtime=0):
	if file==None:
		# afficher l'interface pour récupérer les points (x, y)
		pass
	else:
		# lecture du fichier
		f=open(file,'r')
		lignes=f.readlines()
		f.close()
		
		for ligne in lignes:
			ligneSplited=ligne.split()
			cities.append(City(ligneSplited[0],float(ligneSplited[1]),float(ligneSplited[2])))
		
		for city in cities:
			print(city)
		
		# initialisation de la population initiale
		initPopulation()
		
		startTime=datetime.now()
		
		flag=True
		while True:
			
			select()
			cross()
			mutate()
			
			# gestion du temps
			timespan=datetime.now()-startTime
			if timespan.total_seconds()>maxtime:
				flag=False
				
				# recherche du meilleur
				# TODO
			
			if not flag:
				break

if __name__=="__main__":
	file=None
	gui=True
	maxtime=0
	
	if len(sys.argv)>1:
		if re.search("^[0-9A-Za-z_][0-9A-Za-z_.-][A-Za-z][0-9A-Za-z_.-]+$",sys.argv[-1]):
			file=sys.argv[-1]
		if '--no-gui' in sys.argv:
			gui=False
		if '--max-time' in sys.argv:
			index=sys.argv.index('--max-time')
			maxtime=int(sys.argv[index+1])
	else:
		sys.exit("Error : you must provide a list of cities in the parameter\n \
rossier_fort.py <cities file>\n \
Parameters : \n \
	--no-gui : start without the GUI\n \
	--max-time <time in ms>: how long should the algorithm run \n \
")
	
	ga_solve(file,gui,maxtime)

	
	print("file %s"%file)
	print("gui %d"%gui)
	print("maxtime %d"%maxtime)	