import sys, pygame
import random
from Scent import Scent

class TerritoryScent(Scent):

	def __init__(self,
				 screen,
				 controller,
				 ant_origin,
				 ant_source_image):

		super(TerritoryScent, self).__init__(screen, controller, ant_origin, ant_source_image)

		self.scent_type = 'Territory'

		self.scent_surface.fill( [255, 150, 0] )
		self.decay_timer = 5000