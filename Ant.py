import sys, pygame
import random

class Ant(object):

	#Ant is crafted from cosmic dust here
	def __init__(self, 
				 screen,
				 home,
				 controller,
				 source_image = pygame.image.load('Ant.png'),
				 name = 'John Ant'):

		self.screen = screen
		self.source_image = source_image
		self.name = name
		self.target = None
		self.home = home
		self.controller = controller

		self.food_scent_chance = 0.01
		self.territory_scent_chance = 0.01

		self.food_trail = []
		self.food_trail_goal = None

		self.harvest_timer = 100
		self.inv_space = 5
		self.carried_item = None

		"""
		Direction States:
		[0, 0]   = Static
		[1, 1] 	 = SE
		[-1, -1] = NE
		[-1, 1]  = SW
		[1, -1]  = NW
		[1, 0] 	 = E
		[0, 1] 	 = S
		[-1, 0]  = W
		[0, -1]  = N
		"""
		self.direction = [0, 0]
		self.speed = 1
		self.state = 'Noob'
		self.hit_box = self.source_image.get_rect()



	#Redraws the ant on the screen, is here to simplify
	def update(self):

		self.screen.blit(self.source_image, self.hit_box)


	#Moves the ant, is here to simplify
	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )


	def idleDecision(self):

		if self.controller.ant_swarm.deficit() and self.home.food_count >= 50:
				self.constructTunnel()


	#Changes the ant's coords to simulate movement
	def wander(self):

		#Will ant do something different?
		decision_chance = random.SystemRandom().randint(0, 8)
		#print(decision_chance)

		terr_width, terr_height, terr_originx, terr_originy = self.controller.ant_swarm.territory

		#Only if ant feels like it
		if decision_chance == 3:
			
			#Maybe ant feels lazy
			move_chance = random.SystemRandom().randint(0, 1)
			#The 8 cardinal directions are ant's oyster
			direction = random.SystemRandom().randint(1, 8)

			self.markTerritoryScent()

			#Ant lazy
			if move_chance == 0:

				self.direction[0] = 0
				self.direction[1] = 0
				self.state = 'Lazing'

			#Ant not lazy
			elif move_chance == 1:


				if direction == 1:
					if self.hit_box.bottom <= terr_height:
						self.direction[0] = 0
						self.direction[1] = self.speed
				if direction == 2:
					if self.hit_box.right <= terr_width:
						self.direction[0] = self.speed
						self.direction[1] = 0
				if direction == 3:
					if self.hit_box.bottom <= terr_height and self.hit_box.right <= terr_width:
						self.direction[0] = self.speed
						self.direction[1] = self.speed
				if direction == 4:
					if self.hit_box.top >= terr_originy and self.hit_box.left >= terr_originx:
						self.direction[0] = -self.speed
						self.direction[1] = -self.speed
				if direction == 5:
					if self.hit_box.bottom <= terr_height and self.hit_box.left >= terr_originx:
						self.direction[0] = -self.speed
						self.direction[1] = self.speed
				if direction == 6:
					if self.hit_box.top >= terr_originy and self.hit_box.right <= terr_width: 
						self.direction[0] = self.speed
						self.direction[1] = -self.speed
				if direction == 7:
					if self.hit_box.left >= terr_originx:
						self.direction[0] = -self.speed
						self.direction[1] = 0
				if direction == 8:
					if self.hit_box.top >= terr_originy:
						self.direction[0] = 0
						self.direction[1] = -self.speed

				self.move( self.direction[0], self.direction[1] )
				self.state = 'Wandering'
		else:
			self.move( self.direction[0], self.direction[1] )
			self.state = 'Wandering'

		#Maybe ant needs to stop being lazy
		self.idleDecision()


	#Ant is rolling out
	def moveToTarget(self):

		#Making things a little easier for Ant to process
		t_coord = [self.target.coord[0], self.target.coord[1]]
		a_coord = [self.hit_box.left, self.hit_box.top]

		#Ant smells prey on the x-axis
		if t_coord[0] < a_coord[0]:
			self.direction[0] = -self.speed
		elif t_coord[0] == a_coord[0]:
			self.direction[0] = 0
		else:
			self.direction[0] = self.speed

		#Ant smells prey on the y-axis
		if t_coord[1] < a_coord[1]:
			self.direction[1] = -self.speed
		elif t_coord[1] == a_coord[1]:
			self.direction[1] = 0
		else:
			self.direction[1] = self.speed

		#Ant rolls out
		self.move( self.direction[0], self.direction[1] )


	#Ant is rolling out
	def returnHome(self):

		#Making things a little easier for Ant to process
		home_coord = [self.home.coord[0], self.home.coord[1]]
		a_coord = [self.hit_box.left, self.hit_box.top]

		#Ant smells prey on the x-axis
		if home_coord[0] < a_coord[0]:
			self.direction[0] = -self.speed
		elif home_coord[0] == a_coord[0]:
			self.direction[0] = 0
		else:
			self.direction[0] = self.speed

		#Ant smells prey on the y-axis
		if home_coord[1] < a_coord[1]:
			self.direction[1] = -self.speed
		elif home_coord[1] == a_coord[1]:
			self.direction[1] = 0
		else:
			self.direction[1] = self.speed

		#Ant rolls out
		self.move( self.direction[0], self.direction[1] )


	def followFoodTrail(self):


		if not self.target:

			self.target = self.food_trail[-2]

		if self.target.coord == self.food_trail_goal.coord and self.target != self.food_trail_goal:
			self.target = self.food_trail_goal


		self.moveToTarget()
		self.markFoodScent()

		if self.hit_box.colliderect(self.target.hit_box):

			if self.target == self.food_trail_goal:

				self.state = 'Harvesting Food'
				print(self.name + ' has begun harvesting the delicious food!')
				self.move( -self.direction[0], -self.direction[1] )

			else:

				self.target = self.food_trail[self.food_trail.index(self.target)+1]


	#Ant must harvest the fruits of ant's labor
	def harvestFood(self):

		if self.target in self.controller.fruit_list.fruits:

			if self.harvest_timer != 0:
				self.harvest_timer -= 1
				#print(self.harvest_timer)
			else:
				self.state = 'Delivering Food'

				self.food_trail_goal.fp -= self.inv_space
				self.target = self.food_trail[-2]
				#print('Fruit FP: ' + str(self.target.fp))

				self.controller.foodbit_list.harvestedFoodBit(self, self.inv_space)

				self.harvest_timer = 100

				#print(self.name + ' has begun delivering the food back to Home!')
		else:

			self.state = 'Lazing'
			self.target = None
			self.harvest_timer = 100


	#Ant must provide for the mother country
	def deliverFood(self):

		if self.target == self.food_trail_goal:

			self.target = self.food_trail[-2]

		if self.target.coord == self.home.coord and self.target != self.home:
			self.target = self.home


		self.moveToTarget()
		self.markFoodScent()
		self.carried_item.moveToAnt()

		if self.hit_box.colliderect(self.target.hit_box):

			if self.target == self.home:

				self.move( -self.direction[0], -self.direction[1] )
				self.home.increaseFood(self.inv_space)
				self.carried_item.ant = None
				self.controller.foodbit_list.deleteFoodBit(self.carried_item)
				self.carried_item = None

				if self.food_trail_goal:

					print('Headed to food')
					self.state = 'Following Food Trail'
					self.target = self.food_trail[0]

				else:

					self.state = 'Lazing'
					self.food_trail = []
					self.food_trail_goal = None

			else:

				self.target = self.food_trail[self.food_trail.index(self.target)-1]


	#Ant has good nose
	def withinSmellRange(self, fruit_list):
		
		#collidelist checks all rects in the list and returns first index of collision
		collision_check = self.hit_box.collidelist(fruit_list.smell_boxes)

		#Ant hungers for victory
		if collision_check != -1 and self.state != 'Hunting' and self.state != 'Harvesting Food' and self.state != 'Delivering Food':

			try:

				self.target = fruit_list.fruits[collision_check]
				self.state = 'Hunting'
				print(self.name + ' has picked up the scent of some tasty prey . . . a ' + fruit_list.fruits[collision_check].fruit_type + '!')
			
			except IndexError:

				self.state = 'Lazing'
				self.target = None


	#Ant must share bounty with others
	def shareFoodLocation(self):

		if self.state == 'Delivering Food' or self.state == 'Following Food Trail':
			
			for ant in self.controller.ant_swarm.population:
				
				if ant.state != 'Delivering Food' and ant.state != 'Following Food Trail' and ant.state != 'Harvesting Food':
					if self.hit_box.colliderect(ant.hit_box) and self != ant:

						ant.food_trail = self.food_trail
						ant.food_trail_goal = self.food_trail_goal
						ant.target = ant.food_trail[1]
						ant.state = 'Following Food Trail'
						print(self.name + ' told ' + ant.name + ' about a food source!')


	#Ant must construct additional tunnels
	def constructTunnel(self):


		if self.state != 'Moving to Construct' and self.state != 'Constructing':
			construct_chance = random.SystemRandom().randint(0, 5000)

			if construct_chance == 8:
				self.state = 'Moving to Construct'


		elif self.state == 'Moving to Construct':

			self.returnHome()

			if self.hit_box.colliderect(self.home.hit_box):
				
				self.move( -self.direction[0], -self.direction[1] )
				
				if self.controller.ant_swarm.deficit():
					self.state = 'Constructing'
					print(self.name + ' has begun constructing an additional tunnel for Home!')
				else:
					self.state = 'Lazing'

		elif self.state == 'Constructing':

			if self.controller.ant_swarm.deficit():
				if self.home.tunnel_timer % 100 == 0:
					print('Tunnel is ' + str( (1.0 - float(self.home.tunnel_timer/1000.0) ) * 100  ) + ' percent complete!')
				self.home.underConstruction()
			else:
				self.state = 'Lazing'


	def markFoodScent(self):

		scent_chance = random.SystemRandom().randint(0, 500)

		if scent_chance == 8:#0 <= scent_chance >= self.food_scent_chance*100:

			self.controller.scent_list.createFoodScent(self)
			self.food_scent_chance = 0.01

		else:

			self.food_scent_chance += 0.01


	def markTerritoryScent(self):

		scent_chance = random.SystemRandom().randint(0, 250)

		if scent_chance == 8:#if 0 <= scent_chance >= self.territory_scent_chance*100:

			self.controller.scent_list.createTerritoryScent(self)
			self.territory_scent_chance = 0.01

		else:

			self.territory_scent_chance += 0.01



	def drawPathHome(self):

		for i in range(1, len(self.food_trail)):

			start_coord = [ self.food_trail[i-1].coord[0], self.food_trail[i-1].coord[1] ]
			end_coord = [ self.food_trail[i].coord[0], self.food_trail[i].coord[1] ]

			pygame.draw.line(pygame.display.get_surface(), 
							 [255, 255, 0],
							 start_coord,
							 end_coord)

