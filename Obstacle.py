import sys, pygame
import random

class Obstacle(object):

	def __init__(self,
				 screen,
				 controller,
				 source_images = ['Obstacle_1.png']):

		self.source_images = source_images
		self.screen = screen
		self.controller = controller

		image_chance = random.SystemRandom().randint(0, len(source_images)-1)

		self.source_image = source_images[image_chance]

		self.hit_box = self.source_image.get_rect()

		self.coord = [ 0, 0 ]

		self.width = self.hit_box.width
		self.height = self.hit_box.height


	def update(self):

		self.screen.blit(self.source_image, self.hit_box)

	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )
		self.coord = [self.hit_box.left + self.width/2, self.hit_box.top + self.height/2]


	def randomizePosition(self, obstacle_list):

		spot_check = False

		#First combine fruit_list and obstacle_list
		all_obstacles = obstacle_list + self.controller.fruit_list.fruits

		while not spot_check:
			
			#Resetting position
			self.hit_box.top = 0
			self.hit_box.left = 0
			spot_check = True

			#Picking random positions while staying away from home
			x = random.SystemRandom().randint(0, 950)
			if 350 < x < 650:
				y = random.choice( [random.SystemRandom().randint(0,350),  random.SystemRandom().randint(650,950)] )
			else:
				y = random.SystemRandom().randint(0, 950)
			

			self.move(x, y)

			for obstacle in all_obstacles:

				collision_check = False

				if obstacle != self:
					collision_check = self.hit_box.colliderect(obstacle.hit_box)

				if collision_check:
					spot_check = False



