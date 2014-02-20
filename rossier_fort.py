# -*- coding: utf-8 -*-

import sys
import re
import random
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

	def __str__(self):
		return str(travel)

	def __len__(self):

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
	
	#for individual in population:
	#	print("%s, %f"%(individual.travel,individual.distance))
		

#def evaluate(individual):
#	pass

def select():
	# Tri de la liste, individus ayant la distance la plus courte en premier.
	sorted_pop = sorted(population, key=lambda individual: individual.distance)
	for i in sorted_pop:
		print(i.distance)
	# On créé un tableau avec la meilleure moitié de la population
	# 
	besthalf_pop = sorted_pop[int(len(sorted_pop)/2):]
	for i in besthalf_pop:
		intermediatePopulation.append(i)


def cross():
	print("len",len(intermediatePopulation))
	for individual_index in range(0,len(intermediatePopulation)-2):
		crossover(intermediatePopulation[individual_index],intermediatePopulation[individual_index+1])

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

	print("tits",child1,child2)

def mutate():
	pass

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
			
		initPopulation()
		# boucle
		select()
		cross()

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