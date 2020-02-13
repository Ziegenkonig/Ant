import sys, pygame
import random
from Fruit import Fruit

class FruitList(object):

	#Swarms aren't born, they are spawned
	def __init__(self,
				 screen,
				 initial_amount,
				 fruit_source_image,
				 controller,
				 fp_per = 100):

		self.size = initial_amount
		self.fruit_source_image = fruit_source_image
		self.screen = screen
		self.controller = controller
		self.fp_per = fp_per

		self.fruits = []
		self.smell_boxes = []

		for i in range(initial_amount):

			self.fruits.append( Fruit( self.screen, self.controller, fruit_source_image, fp=fp_per) )

	def updateAll(self):

		for i, fruit in enumerate(self.fruits):
			
			if fruit.fp > 0:
				fruit.update()
			else:
				self.fruits.remove(fruit)
				del self.smell_boxes[i]

	def randomizePositions(self):

		for i, fruit in enumerate(self.fruits):

			#Want to exclude where the ants will be spawning from the spawn points
			x = random.choice( [random.SystemRandom().randint(300,400),  random.SystemRandom().randint(600,700)] )
			y = random.choice( [random.SystemRandom().randint(300,400),  random.SystemRandom().randint(600,700)] )

			fruit.move(x, y)

			self.smell_boxes.append( self.fruits[i].smell_box )

	
