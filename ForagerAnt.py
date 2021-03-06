import sys, pygame
import random
from Ant import Ant

class ForagerAnt(Ant):

	def __init__(self,
				 screen,
				 home,
				 controller,
				 source_image = pygame.image.load('Ant.png'),
				 name = 'John Ant'):

		super(ForagerAnt, self).__init__(screen, home, controller, source_image, name)

		self.explored_scent_chance = 0.01

		self.caste = 'Forager'

		self.smell_surface = pygame.Surface([self.hit_box.width*10, self.hit_box.height*10])
		self.smell_surface.fill([255, 0, 0])
		self.smell_surface.set_alpha(35)
		self.smell_box = self.smell_surface.get_rect()
		self.smell_box = self.smell_box.move( -(self.smell_box.width - self.hit_box.width )/2, -(self.smell_box.height - self.hit_box.height )/2 )


	def update(self):

		self.screen.blit(self.source_image, self.hit_box)
		self.screen.blit(self.smell_surface, self.smell_box)

		#Debugging
		#Keeping this here so the app doesn't overload from ants constantly redrawing a path
		if self.food_trail:
			
			self.drawPathHome()

	#Moves the ant, is here to simplify
	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )
		self.smell_box = self.smell_box.move( x, y )



	#Changes the ant's coords to simulate movement
	def wander(self):

		#Will ant do something different?
		decision_chance = random.SystemRandom().randint(0, 8)
		#print(decision_chance)

		self.markExploredScent()

		#Only if ant feels like it
		if decision_chance == 3:
			
			#Maybe ant feels lazy
			move_chance = random.SystemRandom().randint(0, 1)
			#The 8 cardinal directions are ant's oyster
			direction = random.SystemRandom().randint(1, 8)

			#print('Move_chance ' + str(move_chance) + ' | self.direction: ' + str(self.direction))
			#print('Direction ' + str(direction))

			#Ant lazy
			if move_chance == 0:

				self.direction[0] = 0
				self.direction[1] = 0
				self.state = 'Lazing'

			#Ant not lazy
			elif move_chance == 1:

				#Not gonna lie, I'm too lazy to go through and label these directions
				#They are covered in the constructor
				if direction == 1:
					if self.hit_box.bottom <= self.screen.get_height():
						self.direction[0] = 0
						self.direction[1] = self.speed
				if direction == 2:
					if self.hit_box.right <= self.screen.get_width():
						self.direction[0] = self.speed
						self.direction[1] = 0
				if direction == 3:
					if self.hit_box.bottom <= self.screen.get_height() and self.hit_box.right <= self.screen.get_width():
						self.direction[0] = self.speed
						self.direction[1] = self.speed
				if direction == 4:
					if self.hit_box.top >= 0 and self.hit_box.left >= 0:
						self.direction[0] = -self.speed
						self.direction[1] = -self.speed
				if direction == 5:
					if self.hit_box.bottom <= self.screen.get_height() and self.hit_box.left >= 0:
						self.direction[0] = -self.speed
						self.direction[1] = self.speed
				if direction == 6:
					if self.hit_box.top >= 0 and self.hit_box.right <= self.screen.get_width(): 
						self.direction[0] = self.speed
						self.direction[1] = -self.speed
				if direction == 7:
					if self.hit_box.left >= 0:
						self.direction[0] = -self.speed
						self.direction[1] = 0
				if direction == 8:
					if self.hit_box.top >= 0:
						self.direction[0] = 0
						self.direction[1] = -self.speed

				self.move( self.direction[0], self.direction[1] )
				#Need to check for obstacles here
				if not self.checkObstacles():
					self.move(-self.direction[0], -self.direction[1])

				self.state = 'Wandering'
		else:
			self.move( self.direction[0], self.direction[1] )
			#Need to check for obstacles here
			if not self.checkObstacles():
				self.move(-self.direction[0], -self.direction[1])
					
			self.state = 'Wandering'


	#Overloading hunt function because initial pathfinding logic needs to be unique to foragers
	def hunt(self):

		if self.target in self.controller.fruit_list.fruits:

			#Ant is not blind
			if not self.hit_box.colliderect(self.target.hit_box):
				
				#self.state = 'Hunting'

				self.moveToTarget()
				self.markExploredScent()
				self.markFoodScent()

				#For now this is fine but we'll need to add in some fancier hit detection later
				if self.hit_box.colliderect(self.target.hit_box):

					if not self.food_trail and not self.target.path:

						self.initializeStartEnd()
						self.food_trail = self.controller.a_star.execute(self, self.target, self.controller)
						self.target.path = self.food_trail
						self.food_trail_goal = self.target

					elif not self.food_trail and self.target.path:
						
						self.food_trail = self.target.path
						self.food_trail_goal = self.target

					self.move( -self.direction[0], -self.direction[1] )
					self.state = 'Harvesting Food'
					print(self.name + ' has begun harvesting the delicious food!')

		else:

			self.state = 'Lazing'
			self.target = None


	def initializeStartEnd(self):

		scents = self.controller.scent_list.explored_scents

		# Setting goal for path
		self.controller.scent_list.createExploredScent(self)
		scents[-1].hit_box.top = 0
		scents[-1].hit_box.left = 0
		scents[-1].move(self.home.coord[0], self.home.coord[1])
		scents[-1].coord = [self.home.coord[0], self.home.coord[1]]
		scents[-1].resetNeighborBox()

		# Setting start for path
		self.controller.scent_list.createExploredScent(self)
		scents[-1].hit_box.top = 0
		scents[-1].hit_box.left = 0
		scents[-1].move(self.target.coord[0], self.target.coord[1])
		scents[-1].coord = [self.target.coord[0], self.target.coord[1]]
		scents[-1].resetNeighborBox()

		self.controller.scent_list.registerExploredScentNeighbors()

	#Ant has good nose
	def withinSmellRange(self, fruit_list):
		
		#collidelist checks all rects in the list and returns first index of collision
		collision_check = self.smell_box.collidelist(fruit_list.smell_boxes)

		#Ant hungers for victory
		if collision_check != -1 and self.state != 'Hunting' and self.state != 'Harvesting Food' and self.state != 'Delivering Food' and self.state != 'Following Food Trail':

			try:

				self.target = fruit_list.fruits[collision_check]
				self.state = 'Hunting'
				print(self.name + ' has picked up the scent of some tasty prey . . . a ' + fruit_list.fruits[collision_check].fruit_type + '!')
			
			except IndexError:

				self.state = 'Lazing'
				self.target = None


	def markExploredScent(self):

		#scent_chance = random.SystemRandom().randint(0, 500)


		#if scent_chance == 8 and not self.exploredScentNearby():#if 0 <= scent_chance >= self.explored_scent_chance*100:
		if not self.exploredScentNearby():

			self.controller.scent_list.createExploredScent(self)
			self.explored_scent_chance = 0.01

		else:

			self.explored_scent_chance += 0.01


	def exploredScentNearby(self):

		explored_scents = self.controller.scent_list.explored_scents

		for explored_scent in explored_scents:

			collision_check = self.smell_box.colliderect(explored_scent.hit_box)

			if collision_check:
				return True
		
		return False