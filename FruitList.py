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

		#Debugging, determines how close the fruit spawn to home
		inner_bound = 350
		outer_bound = 650

		for i, fruit in enumerate(self.fruits):

			#Want to exclude where the ants will be spawning from the spawn points
			#Picking random positions while staying away from home
			x = random.SystemRandom().randint(50, 950)
			if inner_bound < x < outer_bound:
				y = random.choice( [random.SystemRandom().randint(50,inner_bound),  random.SystemRandom().randint(outer_bound,950)] )
			else:
				y = random.SystemRandom().randint(50, 950)

			fruit.move(x, y)

			self.smell_boxes.append( self.fruits[i].smell_box )

	
