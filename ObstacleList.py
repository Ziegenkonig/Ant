import sys, pygame
import random
from Obstacle import Obstacle

class ObstacleList(object):

	def __init__(self,
				 screen,
				 controller,
				 source_images = ['Obstacle_1.png'],
				 initial_amount = 5):

		self.screen = screen
		self.controller = controller
		self.source_images = source_images


		self.obstacles = []

		#Instantiate the initial amount of obstacles, and then move them randomly

		for i in range(0, initial_amount):

			self.obstacles.append( Obstacle(self.screen, self.controller, self.source_images) )
			self.obstacles[-1].randomizePosition(self.obstacles)


	def updateAll(self):

		for obstacle in self.obstacles:

			obstacle.update()


	def randomizePositions(self):

		for obstacle in self.obstacles:

			obstacle.randomizePosition(self.obstacles)


	def createObstacle(self):

		self.obstacles.append( Obstacle(self.screen, self.controller, self.source_images) )
		self.obstacles[-1].randomizePosition()