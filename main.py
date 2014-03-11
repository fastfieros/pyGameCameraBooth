#!/usr/bin/env python

import os,sys
import pygame
from thumbnail import getThumbnail
from gphoto import captureAndDownload, registerPhotoEvent
import ubw
import Queue
from events import *

screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
running = 1

pygame.mouse.set_visible(False)

pygame.font.init()

myq = Queue.Queue()
myq.put(startover())

myfont = pygame.font.SysFont("helvetica", 15)

img=None

def getImage(original):
	
	print "Thumbing %s"%original
	thumb = getThumbnail(original)
	if not thumb:
		return None

	print "finished Thumbing %s, to %s "%(original, thumb)
	myq.put(startover())
	return pygame.image.load(thumb)


state = 0

while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0


	### HANDLE QUEUED TASKS ###
	screen.fill((32,32,32))
	if not myq.empty():
		item = myq.get_nowait()

		if item.type == "startover":
			state = 0
			ubw.registerPinEvent(myq)

		elif item.type == "press":
			state = 1
			registerPhotoEvent(myq)

		elif item.type == "photo":
			state = 2
			img = getImage(item.name)


	### GENERATE DISPLAY BASED ON STATE ####

	if state == 0:
		label = myfont.render("waiting for button press..", 1, (255,255,0))
		screen.blit(label, (40,540))

		if img:
			screen.blit(img, (0,0))

	elif state == 1:
		label = myfont.render("taking picture!", 1, (255,255,0))
		screen.blit(label, (40,540))

	elif state == 2:
		label = myfont.render("generating thumbnail..", 1, (255,255,0))
		screen.blit(label, (40,540))

	pygame.display.flip()

