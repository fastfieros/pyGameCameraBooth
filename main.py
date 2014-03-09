#!/usr/bin/env python


import pygame

#screen = pygame.display.set_mode((1024, 768))
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
running = 1

pygame.mouse.set_visible(False)

while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0

	screen.fill((32,32,32))

	blue = 0, 0, 255	
	point1 = 0, 0
	point2 = 200, 100
	#pygame.draw.line(screen, blue, point1, point2)
	pygame.draw.line(screen, (0, 0, 255), (0, 0), (639, 479))
	pygame.draw.aaline(screen, (0, 0, 255), (639, 0), (0, 479))

	pygame.display.flip()
