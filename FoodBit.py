import sys, pygame
import random

class FoodBit(object):

	#A precious commodity to ant
	def __init__(self,
				 screen,
				 controller,
				 ant,
				 food_value = 5,
				 source_image = pygame.image.load('Food_Bit.png')):


		self.screen = screen
		self.source_image = source_image
		self.controller = controller
		self.ant = ant

		self.food_value = food_value
		self.being_carried = True

		self.direction = self.ant.direction
		self.speed = self.ant.speed

		self.hit_box = self.source_image.get_rect()

		x_diff = (self.ant.hit_box.width - self.hit_box.width)/2
		y_diff = (self.ant.hit_box.height - self.hit_box.height)/2

		self.move( self.ant.hit_box.left + x_diff, self.ant.hit_box.top + y_diff)



	def update(self):

		self.screen.blit(self.source_image, self.hit_box)


	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )

	def moveToAnt(self):

		self.direction = self.ant.direction
		self.move( self.direction[0], self.direction[1] )
		self.update()

	def dropped(self):

		self.ant = None