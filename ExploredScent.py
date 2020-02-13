import sys, pygame
import random
from Scent import Scent

class ExploredScent(Scent):

	def __init__(self,
				 screen,
				 controller,
				 ant_origin,
				 ant_source_image):



		self.neighbor_check_box = None

		super(ExploredScent, self).__init__(screen, controller, ant_origin, ant_source_image)

		self.scent_type = 'Explored'

		self.scent_surface.fill( [0, 0, 255] )
		self.scent_surface.set_alpha(200)
		self.decay_timer = 100000

		self.neighbor_check_surface = pygame.Surface([self.ant_origin.hit_box.width*10, self.ant_origin.hit_box.height*10])
		self.neighbor_check_surface.fill([0,0,255])
		self.neighbor_check_surface.set_alpha(100)
		self.neighbor_check_box = self.neighbor_check_surface.get_rect()

		self.neighbor_check_box = self.neighbor_check_box.move( self.hit_box.left, self.hit_box.top )
		self.neighbor_check_box = self.neighbor_check_box.move( -(self.neighbor_check_box.width-self.hit_box.width)/2, -(self.neighbor_check_box.height-self.hit_box.height)/2 )

		self.neighbors = []

	def resetNeighborBox(self):

		self.neighbor_check_box.left = 0
		self.neighbor_check_box.top = 0
		self.neighbor_check_box = self.neighbor_check_box.move( self.hit_box.left, self.hit_box.top )
		self.neighbor_check_box = self.neighbor_check_box.move( -(self.neighbor_check_box.width-self.hit_box.width)/2, -(self.neighbor_check_box.height-self.hit_box.height)/2 )


	def update(self):

		self.screen.blit(self.scent_surface, self.hit_box)
		self.decay_timer -= 1

		#Debugging
		#self.screen.blit(self.neighbor_check_surface, self.neighbor_check_box)
		#self.drawLinesToNeighbors()

	#Only need to call this every time a new explored scent is either created or destroyed
	#Also forgot to reset the list everytime this is called, that's pretty important and would explain the lag
	def registerNeighbors(self):

		self.neighbors = []

		potential_neighbors = self.controller.scent_list.explored_scents

		for potential_neighbor in potential_neighbors:

			collision_check = self.neighbor_check_box.colliderect(potential_neighbor.neighbor_check_box)

			if collision_check and potential_neighbor not in self.neighbors and potential_neighbor != self:

				self.neighbors.append(potential_neighbor)

	#For bug testing, also looks trippy af
	def drawLinesToNeighbors(self):

		for neighbor in self.neighbors:

			start_coord = [self.coord[0], self.coord[1]]
			end_coord = [neighbor.coord[0], neighbor.coord[1]]

			pygame.draw.line(pygame.display.get_surface(), 
							 [255, 255, 255],
							 start_coord,
							 end_coord)


