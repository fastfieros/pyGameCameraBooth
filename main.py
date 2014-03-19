#!/usr/bin/env python

#System Libraries
import time
import pygame

#Data structures
import Queue
from collections import deque

#Project Files
import ubw
from gphoto import *
from events import *
from states import *
from config import *

def init():
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    myq = Queue.Queue()
    myq.put(startover())

    pygame.font.init()
    myfont      = pygame.font.SysFont("helvetica", 24)
    consolefont = pygame.font.SysFont("DejaVu Sans Mono", 12)
    bigfont     = pygame.font.SysFont("helvetica", 125)
    hugefont    = pygame.font.SysFont("DejaVu Sans", 300)

    preview_img    = None               #Last photograph taken
    thumbnail_imgs = deque(maxlen=6)    #list of thumbnails
    pe             = None               #pin event
    countdownEnd   = None

    running = 1
    state = STATE_RESET

    disableAutoOff()

def loop():
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pe.kill = True
        running = 0


    ### HANDLE QUEUED TASKS ###
    screen.fill(background)
    if not myq.empty():
        item = myq.get_nowait()

        if item.type == "startover":
            state = STATE_RESET
            pe = ubw.registerPinEvent(myq)

        elif item.type == "press":
            state = STATE_COUNTDOWN
            countdownEnd = time.time() + timer_secs

        elif item.type == "photo":
            if not item.name:
                pe.kill = True
                state = STATE_ERROR
                message = item.message

            else:
                state = STATE_PROCESS

        elif item.type == "downloading":
            state = STATE_TRANSFER

        elif item.type == "preview":
            countdownEnd = time.time() + preview_secs
            preview_img = item.image 
            state = STATE_PREVIEW

        elif item.type == "thumbnail":
            thumbnail_imgs.pppend(item.image)
            # no state change.


    ### GENERATE DISPLAY BASED ON STATE ####

    if state == STATE_RESET:
        label = myfont.render("Press button to capture!", 1, (255,255,0))
        screen.blit(label, (40,540))

        #show last 6 images!
        for i,img in enumerage(thumbnail_imgs):
            x = 50 + (200 + 25) * i
            y = 50 + (300 + 25) * i%3 
            screen.blit(img, (x,y))

    elif state == STATE_COUNTDOWN:

        timeleft = countdownEnd - time.time() 
        if timeleft <= capture_secs
            #Start capture n seconds before timer runs out
            registerPhotoEvent(myq)

        if timeleft >= 0:
            #Provide countdown until capture
            label = hugefont.render("%.1f"%timeleft, 1, (0,255,0))
            screen.blit(label, (120,120))

        else:
            state = STATE_CAPTURE

    elif state == STATE_CAPTURE:
        #Update user w/ status info
        dots = "."*(int(time.time())%3)
        label = myfont.render("Capturing picture%s"%dots, 1, (255,0,255))
        screen.blit(label, (40,540))

    elif state == STATE_TRANSFER:
        #Update user w/ status info
        dots = "."*(int(time.time())%3)
        label = myfont.render("transferring picture%s"%dots, 1, (255,255,0))
        screen.blit(label, (40,540))

    elif state == STATE_PROCESS:
        #Update user w/ status info
        dots = "."*(int(time.time())%3)
        label = myfont.render("processing picture%s"%dots, 1, (0,255,255))
        screen.blit(label, (40,540))

    elif state == STATE_PREVIEW:
        # display the image 'preview' until countdown expires
        screen.blit(preview_img, (0,0))

        # When countdown expires, start over :)
        timeleft = countdownEnd - time.time() 
        if timeleft <= 0:
            myq.put(startover())

    ## ERROR STATE ##
    elif state == STATE_ERROR:
        label = bigfont.render("ERROR!!", 1, (255,0,0))
        screen.blit(label, (40,40))

        #parse the message so it fits on the screen
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
            label = myfont.render("press button to continue.", 1, (255,255,0))
            screen.blit(label, (40,540))


    pygame.display.flip()



if __name__ == "__main__":

    init()

    try:
        while running:
            loop()

    except KeyboardInterrupt as ke:
    	pe.kill = True		
