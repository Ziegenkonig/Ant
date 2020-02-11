import sys, pygame
import random

class AStar(object):

	def __init__(self):
		None

	def execute(self, ant, fruit, controller):

		home = controller.home
		home_x = home.hit_box.left + (home.hit_box.width/2)
		home_y = home.hit_box.top + (home.hit_box.height/2)
		home_vector = pygame.Vector2( home_x, home_y )

		all_nodes = controller.scent_list.explored_scents
		all_nodes.append(home)

		fruit_vector = pygame.Vector2( fruit.hit_box.left + fruit.hit_box.width/2, fruit.hit_box.top + fruit.hit_box.height/2 )

		end_node = self.findEndNode(all_nodes, home_vector)
		start_node = self.findStartNode(all_nodes, fruit_vector)

		g_value_dict = {}

		#begin actual algorithm
		#initialize open list
		open_list = []

		#initialize closed list
		closed_list = []

		#place starting node in list
		#initialize start_node's g value to 0
		open_list.append(start_node)
		g_value_dict[start_node] = 0

		#run until open_list is empty
		while open_list:

			lowest_cost_node = None
			#find node with least f value
			for node in open_list:

				f_value = self.gValue(closed_list, node) + self.hValue(node, end_node)

				if lowest_cost_node is None:
					lowest_cost_node = node
					prev_f_value = f_value
				elif f_value < prev_f_value:
					lowest_cost_node = node
					prev_f_value = f_value


			if lowest_cost_node == end_node:
				return self.constructPath(closed_list, lowest_cost_node)

			open_list.remove(lowest_cost_node)
			for neighbor in lowest_cost_node.neighbors:

				tentative_g_score = self.gValue(lowest_cost_node) + self.distance(lowest_cost_node, neighbor)

				if tentative_g_score < self.gValue(neighbor):

					closed_list.append(lowest_cost_node)

					if neighbor not in open_list:
						open_list.append(neighbor)



	def findStartNode(self, all_nodes, fruit_vector):

		start_node = None
		#Find the closest node first, ie starting node
		for node in all_nodes:

			node_x = node.hit_box.left
			node_y = node.hit_box.top

			node_vector = pygame.Vector2( node_x, node_y )

			dist_to_fruit = node_vector.distance_to(fruit_vector)

			if start_node is None:
				start_node = node
				prev_dist_to_fruit = dist_to_fruit
			elif dist_to_fruit < prev_dist_to_fruit:
				start_node = node
				prev_dist_to_fruit = dist_to_fruit

		return start_node


	def findEndNode(self, all_nodes, home_vector):

		end_node = None
		#Find the closest node first, ie starting node
		for node in all_nodes:

			node_x = node.hit_box.left
			node_y = node.hit_box.top

			node_vector = pygame.Vector2( node_x, node_y )

			dist_to_home = node_vector.distance_to(home_vector)

			if end_node is None:
				start_node = node
				prev_dist_to_home = dist_to_home
			elif dist_to_home < prev_dist_to_home:
				start_node = node
				prev_dist_to_home = dist_to_home

		return end_node


	def hValue(self, node, end_node):

		home_x = end_node.hit_box.left + (end_node.hit_box.width/2)
		home_y = end_node.hit_box.top + (end_node.hit_box.height/2)

		home_vector = pygame.Vector2( home_x, home_y )

		node_x = node.hit_box.left + (node.hit_box.width/2)
		node_y = node.hit_box.top + (node.hit_box.height/2)

		node_vector = pygame.Vector2( node_x, node_y )

		return node_vector.distance_to(home_vector)

	def gValue(self, closed_list, node):

		total_distance = 0
		for i in range(1, len(closed_range)-1):

			total_distance += self.distance(closed_list[i-1], closed_list[i])

		total_distance += self.distance(closed_list[-1], node)

		return total_distance


	def distance(self, node_a, node_b):

		node_ax = node_a.hit_box.left + (node_a.hit_box.width/2)
		node_ay = node_a.hit_box.top + (node_a.hit_box.height/2)

		node_bx = node_b.hit_box.left + (node_b.hit_box.width/2)
		node_by = node_b.hit_box.top + (node_b.hit_box.height/2)

		node_a_vector = pygame.Vector2( node_ax, node_ay )
		node_b_vector = pygame.Vector2( node_bx, node_by )

		return node_a_vector.distance_to(node_b_vector)

	def constructPath(self, closed_list, current):

		total_path = []
		total_path.append(current)

		while closed_list:

			total_path.append( closed_list.pop() )

		return total_path












