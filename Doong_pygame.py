#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, sys, time, math, pygame
pygame.init();
from pygame.locals import *
import time

#defining colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (34, 139, 34)
blue = (0, 0, 255)

width = 800
height = 600
clock = pygame.time.Clock()

pygame.display.set_caption("Doong Pygame")

class randomEatees(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()

def main():
	fps = 30 # frames per second to update the screen
	start_size = 15
	start_x = width/2
	start_y = height/2
	x_change = 0
	y_change = 0
	movement = 10

	randX = round(random.randrange(0, width - start_size)/10.0)*10.0
	randY = round(random.randrange(0, height - start_size)/10.0)*10.0

	#randX = random.randrange(0, width - size)
	#randY = random.randrange(0, height - size)

	gameDisplay = pygame.display.set_mode((width,height))

	gameExit = False

	block_list = pygame.sprite.Group()
	all_sprites_list = pygame.sprite.Group()

	for i in range(50):

			block = randomEatees(black, 15, 15)
 
			block.rect.x = round(random.randrange(width)/10.0)*10.0
			block.rect.y = round(random.randrange(height)/10.0)*10.0

			block_list.add(block)
			all_sprites_list.add(block)

	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -movement
					y_change = 0
				elif event.key == pygame.K_RIGHT:
					x_change = movement
					y_change = 0
				elif event.key == pygame.K_UP:
					y_change = -movement
					x_change = 0
				elif event.key == pygame.K_DOWN:
					y_change = movement
					x_change = 0

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_DOWN:
					x_change = 0
					y_change = 0
	
		f = pygame.font.Font(None, 32)
		if start_x >= width or start_x <= 0 or start_y >= height or start_y <= 0:
			gameExit = True
			# label = f.render("Game over!", True, red)
			# gameDisplay.blit(label, [width/2, height/2])
			# pygame.display.update()

		start_x += x_change
		start_y += y_change

		gameDisplay.fill(green)
		pygame.draw.rect(gameDisplay, red, [randX, randY, start_size, start_size])
		pygame.draw.rect(gameDisplay, blue, [start_x, start_y, start_size, start_size])
		#pygame.draw.rect(gameDisplay, red, [100,200, 15, 15])
		pygame.display.update()

		if start_x == randX and start_y == randY:
			randX = round(random.randrange(0, width - start_size)/10.0)*10.0
			randY = round(random.randrange(0, height - start_size)/10.0)*10.0

		all_sprites_list.draw(gameDisplay)

		if start_x == block.rect.x and start_y == block.rect.y:
			gameExit = True

		#pygame.display.flip()

		clock.tick(fps)

	pygame.quit()
	quit()

main()
