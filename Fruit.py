import sys, pygame
import random

class Fruit(object):

	#Fruit falls from the tree here, poofing into existence
	def __init__(self,
				 screen,
				 controller,
				 source_image = pygame.image.load('Fruit_Large.png'),
				 fruit_type = 'Apple',
				 coord = [0, 0],
				 fp = 100):

		self.screen = screen
		self.source_image = source_image
		self.fruit_type = fruit_type
		self.controller = controller

		#self.smell_box_image = pygame.image.load('Fruit_Smellbox.png')
		#self.smell_box_image.set_alpha(15)

		self.fp = fp

		self.hit_box = self.source_image.get_rect()

		self.smell_surface = pygame.Surface([self.hit_box.width*8, self.hit_box.height*8])
		self.smell_surface.fill([0, 255, 0])
		self.smell_surface.set_alpha(35)
		self.smell_box = self.smell_surface.get_rect()

		#self.smell_box.width *= 3
		#self.smell_box.height *= 3

		self.coord = [self.hit_box.left, self.hit_box.top]

		self.width = self.hit_box.width
		self.height = self.hit_box.height


	def update(self):

		self.screen.blit(self.source_image, self.hit_box)
		self.screen.blit(self.smell_surface, self.smell_box)


	#Fruit can't move, because they don't have legs
	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )
		self.smell_box = self.smell_box.move( x - ((self.smell_box.width/2)-self.hit_box.width/2), y - ((self.smell_box.height/2)-self.hit_box.height/2) )
		#print(str(self.smell_box.left) + ', ' + str(self.smell_box.right))
		#print(str(self.hit_box.left) + ', ' + str(self.hit_box.right))
		self.coord = [self.hit_box.left, self.hit_box.top]