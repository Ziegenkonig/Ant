import sys, pygame
import random
from FoodBit import FoodBit

class FoodBitList(object):

	#A precious commodity to ant
	def __init__(self,
				 screen,
				 foodbit_source_image,
				 controller):

		self.screen = screen
		self.foodbit_source_image = foodbit_source_image
		self.controller = controller

		self.food_bits = []


	def newFoodBit(self, ant, food_value = 5):

		self.food_bits.append( FoodBit(self.screen, self.controller, ant, food_value, self.foodbit_source_image) )


	def harvestedFoodBit(self, ant, food_value = 5):

		new_foodbit = FoodBit(self.screen, self.controller, ant, food_value, self.foodbit_source_image)

		self.food_bits.append(new_foodbit)
		ant.carried_item = new_foodbit


	def deleteFoodBit(self, food_bit):

		self.food_bits.remove(food_bit)


	def updateAll(self):

		for foodbit in self.food_bits:

			if foodbit.ant != None:
				foodbit.update()