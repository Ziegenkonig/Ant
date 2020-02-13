import sys, pygame
import random

class Scent(object):

	def __init__(self,
				 screen,
				 controller,
				 ant_origin,
				 ant_source_image):

		self.screen = screen
		self.controller = controller
		self.ant_origin = ant_origin
		self.ant_owner_name = ant_origin.name

		self.scent_type = None

		ant_hit_box = ant_source_image.get_rect()

		self.scent_surface = pygame.Surface( [ant_hit_box.width/2, ant_hit_box.height/2] )
		self.hit_box = self.scent_surface.get_rect()
		self.scent_surface.set_alpha(100)

		self.decay_timer = 500

		self.coord = [self.ant_origin.hit_box.left, self.ant_origin.hit_box.top]

		self.move( self.coord[0], self.coord[1] )

		#Want to randomly place the scent somewhere in the close vicinity of the ant

		scent_x = random.SystemRandom().randint(-20, 20)
		scent_y = random.SystemRandom().randint(-20, 20)
		#self.coord = [scent_x, scent_y]
		#self.move( (self.ant_origin.hit_box.width - self.hit_box.width)/2, (self.ant_origin.hit_box.height - self.hit_box.height)/2 )
		self.move( scent_x, scent_y )


	def update(self):

		self.screen.blit(self.scent_surface, self.hit_box)
		self.decay_timer -= 1

	def move(self, x, y):

		self.hit_box = self.hit_box.move( x, y )
		self.coord = [self.hit_box.left + self.hit_box.width/2, self.hit_box.top + self.hit_box.height/2]