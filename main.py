#!/usr/bin/env python

import os,sys,time
import pygame
from thumbnail import getThumbnail
from gphoto import captureAndDownload, registerPhotoEvent
import ubw
import Queue
from events import *
from loadingbox import progressBar, timeoutBar

screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

running = 1

pygame.mouse.set_visible(False)

pygame.font.init()

myq = Queue.Queue()
myq.put(startover())

myfont = pygame.font.SysFont("helvetica", 15)
consolefont = pygame.font.SysFont("DejaVu Sans Mono", 12)
bigfont = pygame.font.SysFont("helvetica", 85)

img=None #Last photograph taken
pe=None  #pin event
countdownEnd=None

def getImage(original):
	
	print "Thumbing %s"%original
	thumb = getThumbnail(original)
	if not thumb:
		return None

	print "finished Thumbing %s, to %s "%(original, thumb)
	myq.put(startover())
	return pygame.image.load(thumb)


state = 0
try:
	while running:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			pe.kill = True
			running = 0


		### HANDLE QUEUED TASKS ###
		screen.fill((32,32,32))
		if not myq.empty():
			item = myq.get_nowait()

			if item.type == "startover":
				state = 0
				pe = ubw.registerPinEvent(myq)

			elif item.type == "press":
				state = 3
				countdownEnd = time.time() + 5

			elif item.type == "photo":
				if not item.name:
					pe.kill = True
					state = 99
					message = item.message
				else:
					state = 2
					img = getImage(item.name)


		### GENERATE DISPLAY BASED ON STATE ####

		if state == 0:
			label = myfont.render("Press button to capture!", 1, (255,255,0))
			screen.blit(label, (40,540))

			# show last 5 or so images!
			if img:
				screen.blit(img, (0,0))

		elif state == 3 or state == 4:
			timeleft = countdownEnd - time.time() 
			if state == 3 and timeleft <= 1.0:
				registerPhotoEvent(myq)
				state = 4

			if state == 4 and timeleft <= 0:
				countdownEnd = time.time() + 1
				state = 5	

			else:
				label = bigfont.render("%.3f"%timeleft, 1, (0,255,0))
				screen.blit(label, (240,240))

		elif state == 5:
			screen.fill((255,255,255))
			timeleft = countdownEnd - time.time() 

			if timeleft <= 0:
				timebar = timeoutBar(screen, 4.8)
				state = 1

			else:
				label = bigfont.render("Smile!", 1, (0,128,128))
				screen.blit(label, (240,240))

		elif state == 1:
			label = myfont.render("taking picture!", 1, (255,255,0))
			screen.blit(label, (40,540))
			
			timebar.update()

		elif state == 2:
			label = myfont.render("generating thumbnail..", 1, (255,255,0))
			screen.blit(label, (40,540))

		#state 4: display fullsize image 
		# 	in 5 seconds, change to state 0

		elif state == 99:
			label = bigfont.render("ERROR!!", 1, (255,0,0))
			screen.blit(label, (40,40))

			i=0
			for m in message.split('\n'):
				for j ,x in enumerate(range(0,len(m),80)):
					label = consolefont.render(m[j*80:(j+1)*80], 1, (255,255,0))
					left = (j==0 and 40 or 80)	
					down = 130+(i*20)
					screen.blit(label, (left, down))
					i+=1
					
			#if the press event was just killed, start a new one :)
			if pe.kill:
				pe = ubw.registerPinEvent(myq)
			else:
				label = myfont.render("waiting for button press..", 1, (255,255,0))
				screen.blit(label, (40,540))


		pygame.display.flip()

except KeyboardInterrupt as ke:
	pe.kill = True		

