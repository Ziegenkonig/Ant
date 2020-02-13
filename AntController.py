import sys, pygame
import random

class AntController(object):

	def __init__(self):

		self.ant_swarm = None
		self.fruit_list = None
		self.home = None
		self.foodbit_list = None
		self.scent_list = None
		self.a_star = None
		self.obstacle_list = None


