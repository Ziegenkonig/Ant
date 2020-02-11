import sys, pygame
import random
from Scent import Scent

class FoodScent(Scent):

	def __init__(self,
				 screen,
				 controller,
				 ant_origin,
				 ant_source_image):

		super(FoodScent, self).__init__(screen, controller, ant_origin, ant_source_image)

		self.scent_type = 'Food'

		self.scent_surface.fill( [255, 255, 0] )
		self.decay_timer = 1000