import sys, pygame
import random
import numpy as np
from Ant import Ant
from AntSwarm import AntSwarm
from Fruit import Fruit
from FruitList import FruitList
from Home import Home
from AntController import AntController
from FoodBitList import FoodBitList
from ScentList import ScentList
from Algorithms import AStar
from ObstacleList import ObstacleList

pygame.init()

window_size = width, height = 1000, 1000
speed = [0, 0]
background_color = 0, 0, 0
screen = pygame.display.set_mode(window_size)

swarm_size = 50

ant_controller = AntController()

home_source_image = pygame.image.load('Home.png')
home = Home(screen, ant_controller, swarm_size, home_source_image, [window_size[0]/2, window_size[1]/2])
#home.move( (window_size[0]/2) - (home.width/2), window_size[1]/2 - home.height/2 )

ant_source_image = pygame.image.load('Ant.png')
swarm = AntSwarm(swarm_size, [window_size[0]/2, window_size[1]/2], screen, ant_source_image, home, ant_controller)

fruit_source_image = pygame.image.load('Fruit_Large.png')
fruit_list = FruitList(screen, 3, fruit_source_image, ant_controller, 1000000)
fruit_list.randomizePositions()
ant_controller.fruit_list = fruit_list

obstacle_source_images = []
obstacle_source_images.append( pygame.image.load('Obstacle_1.png') )
obstacle_source_images.append( pygame.image.load('Obstacle_2.png') )
obstacle_source_images.append( pygame.image.load('Obstacle_3.png') )
obstacle_source_images.append( pygame.image.load('Obstacle_4.png') )
obstacle_list = ObstacleList( screen, ant_controller, obstacle_source_images, 40 )

foodbit_source_image = pygame.image.load('Food_Bit.png')
foodbit_list = FoodBitList(screen, foodbit_source_image, ant_controller)

scent_list = ScentList(screen, ant_controller, ant_source_image)

a_star = AStar()

ant_controller.ant_swarm = swarm
ant_controller.home = home
ant_controller.foodbit_list = foodbit_list
ant_controller.scent_list = scent_list
ant_controller.a_star = a_star
ant_controller.obstacle_list = obstacle_list

clock = pygame.time.Clock()

#Main loop
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	#This needs to go before we draw anything, so the stuff gets drawn on top
	screen.fill(background_color)

	#Placing the scent updates here because I want them to render behind literally everything for now
	scent_list.updateAll()

	#I think it matters where we place the drawing of an image so, im placing home at the top
	home.update()

	#I'm torn about where to put this so it's here for now
	obstacle_list.updateAll()

	#Temporary birth code, I'll keep it because it doesn't harm anything but I need to move it to swarm.live()
	birth_chance = random.SystemRandom().randint(0, 500)
	if birth_chance == 8:
		swarm.give_birth()

	#Ants need to check their environment every tick, for hitbox detection
	swarm.environmentCheck(fruit_list)
	#This function handles all of the ants' possible behaviors
	swarm.live()

	#This ensures that the fruit is being drawn on the screen
	fruit_list.updateAll()
	foodbit_list.updateAll()

	pygame.display.flip()
	clock.tick(144)




