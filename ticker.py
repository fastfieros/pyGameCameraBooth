#!/usr/bin/env python

#System Libraries
import time
import pygame
import random

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
pcfont      = pygame.font.SysFont("courier new", 48)

camera_img    = pygame.image.load("camera.png")
tv_img        = pygame.image.load("tv.png")

start=time.time()

def loop():
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pe.kill = True
        running = 0


    screen.fill((32,32,32))
    s = pygame.Surface((1024,768), flags=pygame.SRCALPHA)
    t = time.time()
    camera_end = 300
    screen_start = 675

    label = myfont.render("time :%.2f"%t, 1, (255,0,0))
    s.blit(label, (40,40))

    #draw the channel on the bottom
    pygame.draw.rect(s, (16,16,16), pygame.Rect(camera_end, 400, screen_start-camera_end, 50))

    #then draw circles on the channel
    num = 10 
    delta = int(500/num)
    for i in range(num):
        circlex = camera_end - delta + (i*delta) + int((time.time() - start) * 50) %delta 
        c = 40+i*((256-40)/num)
        color = (c,c,c)
        #pygame.draw.circle(s, color, (circlex,425), 18, 5)
        bit = pcfont.render("%d"%random.randint(0,1), 1, color)
        s.blit(bit, (circlex, 400))

    #then draw the icons
    s.blit(camera_img, (10, 265))
    s.blit(tv_img, (600, 250))

    #then draw the lines
    pygame.draw.line(s, (0,0,0), (camera_end,400), (screen_start,400), 5)
    pygame.draw.line(s, (0,0,0), (camera_end,450), (screen_start,450), 5)
    
    screen.blit(s, (0,0))

    pygame.display.flip()



if __name__ == "__main__":

    camera_img.convert_alpha()
    tv_img.convert_alpha()

    try:
        while running:
            loop()

    except KeyboardInterrupt as ke:
        pass
