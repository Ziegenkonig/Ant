import sys, pygame
import random
from Scent import Scent
from ExploredScent import ExploredScent
from FoodScent import FoodScent
from TerritoryScent import TerritoryScent

class ScentList(object):

	def __init__(self,
				 screen,
				 controller,
				 ant_source_image):

		self.screen = screen
		self.controller = controller
		self.ant_source_image = ant_source_image

		self.scents = []
		self.explored_scents = []



	def updateAll(self):

		for scent in self.scents:

			if scent.decay_timer > 0:
				scent.update()
			else:
				if scent.scent_type == 'Explored':
					self.scents.remove(scent)
					self.explored_scents.remove(scent)
					self.registerExploredScentNeighbors()
				else:
					self.scents.remove(scent)
				

	def createExploredScent(self, ant):

		new_scent = ExploredScent(self.screen, self.controller, ant, self.ant_source_image)

		self.scents.append(new_scent)
		self.explored_scents.append(new_scent)

		self.registerExploredScentNeighbors()

	def registerExploredScentNeighbors(self):

		for scent in self.explored_scents:
			scent.registerNeighbors()

	def createFoodScent(self, ant):

		new_scent = FoodScent(self.screen, self.controller, ant, self.ant_source_image)

		self.scents.append(new_scent)

	def createTerritoryScent(self, ant):

		new_scent = TerritoryScent(self.screen, self.controller, ant, self.ant_source_image)

		self.scents.append(new_scent)

