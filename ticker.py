#!/usr/bin/env python

#System Libraries
import time
import pygame

#Data structures
import Queue
from collections import deque

import os

running=1
screen=None

screen = pygame.display.set_mode((1024,768), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

pygame.font.init()
myfont      = pygame.font.SysFont("helvetica", 24)

camera_img    = pygame.image.load("camera.jpg")
tv_img        = pygame.image.load("tv.png")

start=time.time()

def loop():
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pe.kill = True
        running = 0


    screen.fill((255,255,255))
    t = time.time()

    label = myfont.render("time :%f"%t, 1, (255,0,0))
    screen.blit(label, (40,40))

    #draw circles on the bottom
    camera_end = 300
    screen_start = 675
    for i in range(6):
        circlex = camera_end - 90 + (i*90) + int((time.time() - start) * 100) % 90
        pygame.draw.circle(screen, (200,200,200), (circlex,425), 20, 5)

    #then draw the icons
    screen.blit(camera_img, (10, 265))
    screen.blit(tv_img, (600, 250))

    #then draw the lines
    pygame.draw.line(screen, (0,0,0), (camera_end,400), (screen_start,400), 5)
    pygame.draw.line(screen, (0,0,0), (camera_end,450), (screen_start,450), 5)
    

    pygame.display.flip()



if __name__ == "__main__":

    try:
        while running:
            loop()

    except KeyboardInterrupt as ke:
        pass
