import sys, pygame
import random

class Home(object):

	#Ant calls this place home, really is just dirt
	def __init__(self, 
				 screen,
				 controller,
				 swarm_size,
				 source_image = pygame.image.load('Home.png'),
				 coord = [0, 0]):

		self.screen = screen
		self.source_image = source_image
		self.coord = coord
		self.controller = controller

		self.food_count = 100
		#Each tunnel allows an extra 5 population, reflected in ant_swarm's give_birth()
		self.tunnel_count = swarm_size/5
		#How long it takes to complete a tunnel, can be worked on by multiple ants
		self.tunnel_timer = 1000
		self.under_construction = False

		self.hit_box = self.source_image.get_rect()
		self.width = self.hit_box.width
		self.height = self.hit_box.height

		self.move(self.coord[0], self.coord[1])



	def update(self):

		self.screen.blit(self.source_image, self.hit_box)


	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )
		self.coord = [(self.hit_box.left + self.hit_box.width/2), (self.hit_box.top + self.hit_box.height/2)]



	# :)
	def increaseFood(self, amount):

		self.food_count += amount
		print('Home now has ' + str(self.food_count) + ' food stored')

	# :(
	def decreaseFood(self, amount):

		self.food_count -= amount
		print('Home now has ' + str(self.food_count) + ' food stored')



	def underConstruction(self):
		
		if self.tunnel_timer > 0:
			
			self.tunnel_timer -= 1

		else:

			self.tunnel_timer = 1000
			self.tunnel_count += 1
			self.food_count -= 50
			self.under_construction = False



