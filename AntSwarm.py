import sys, pygame
import random
from Ant import Ant
from ForagerAnt import ForagerAnt

class AntSwarm(object):

	#Swarms aren't born, they are spawned
	def __init__(self,
				 initial_pop,
				 initial_coord,
				 screen,
				 ant_source_image,
				 home,
				 controller):

		self.size = initial_pop
		self.ant_source_image = ant_source_image
		self.screen = screen
		self.home = home
		self.controller = controller

		self.forager_percent = 0.1

		screen_width, screen_height = pygame.display.get_surface().get_size()
		self.territory = [screen_width/2 + self.home.width*3, 
						  screen_height/2 + self.home.height*3,
						  screen_width/2 - self.home.width*3, 
						  screen_height/2 - self.home.height*3]

		self.population = []
		self.forager_population = []
		self.ant_boxes = []

		#Filling colony with he initial population
		for i in range(initial_pop):

			forager_chance = random.SystemRandom().randint(0, self.forager_percent*100)
			if forager_chance == 8:
				self.population.append( ForagerAnt( self.screen, self.home, controller, self.ant_source_image, 'Forager Ant #' + str(i) ))
				self.population[i].move( initial_coord[0], initial_coord[1])
				self.ant_boxes.append( self.population[i].hit_box )
				self.forager_population.append(self.population[i])
			else:
				self.population.append( Ant( self.screen, self.home, controller, self.ant_source_image, 'Ant #' + str(i) ) )
				self.population[i].move( initial_coord[0], initial_coord[1])
				self.ant_boxes.append( self.population[i].hit_box )




	def move_all(self, x, y):

		for ant in self.population:
			ant.move( x, y )


	#New Ant
	def give_birth(self,
				   amount = 1, 
				   name = '@'):

		if name == '@':
			name = 'Ant #' + str(self.size)

		if not self.deficit():
			for i in range(amount):
				forager_chance = random.SystemRandom().randint(0, self.forager_percent*100)
				if forager_chance == 8:
					self.population.append( ForagerAnt( self.screen, self.home, self.controller, self.ant_source_image, 'Forager Ant #' + str(i) ))
					self.population[-1].move( self.screen.get_width()/2, self.screen.get_height()/2 )
					self.ant_boxes.append( self.population[i].hit_box )
					self.forager_population.append(self.population[i])
				else:
					self.population.append( Ant( self.screen, self.home, self.controller, self.ant_source_image, name ) )
					self.population[-1].move( self.screen.get_width()/2, self.screen.get_height()/2 )
					self.size += 1
					self.ant_boxes.append( self.population[self.size-1].hit_box )

				print('Welcome to the world baby ant! Your name is ' + name)
				print( 'Current Population: ' + str(self.size) )


	#Ant have simple habits
	def wander_all(self):

		for ant in self.population:
			ant.wander()
			ant.update()


	#Decided Ant needed a separate function for this, it has potential to be expanded a lot
	def environmentCheck(self, fruit_list):

		for ant in self.population:

			ant.withinSmellRange(fruit_list)

		for ant in self.forager_population:

			ant.shareFoodLocation()


	#Ant lead humble life, is all defined here
	def live(self):

		for ant in self.population:

			if ant.state == 'Noob' or ant.state == 'Wandering' or ant.state == 'Lazing':

				ant.wander()

			elif ant.state == 'Hunting':

				ant.hunt()

			elif ant.state == 'Harvesting Food':

				ant.harvestFood()

			elif ant.state == 'Delivering Food':

				ant.deliverFood()

			elif ant.state == 'Moving to Construct' or ant.state == 'Constructing':

				ant.constructTunnel()


			ant.update()



	def deficit(self):

		if (self.home.tunnel_count*5) <= self.size:

			return True

		else:

			return False
