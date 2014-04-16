#!/usr/bin/env python

#System Libraries
import time
import pygame
import random

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
    global screen
    global myq
    global myfont    
    global consolefont
    global bigfont   
    global hugefont   
    global preview_img  
    global thumbnail_imgs
    global pe         
    global countdownEnd
    global running
    global state
    global startTime
    global tv_img
    global camera_img

    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN )
    pygame.mouse.set_visible(False)

    myq = Queue.Queue()
    myq.put(startover())

    pygame.font.init()
    myfont      = pygame.font.SysFont("helvetica", 24)
    consolefont = pygame.font.SysFont("DejaVu Sans Mono", 12)
    bigfont     = pygame.font.SysFont("helvetica", 125)
    hugefont    = pygame.font.SysFont("DejaVu Sans", 480)

    preview_img    = None               #Last photograph taken
    thumbnail_imgs = deque(maxlen=6)    #list of thumbnails
    pe             = None               #pin event
    countdownEnd   = None
    camera_img    = pygame.image.load("camera.png")
    tv_img        = pygame.image.load("tv.png")

    startTime=time.time()

    running = 1
    state = STATE_RESET

    disableAutoOff()

def transferAnimation():
    global screen
    global myq
    global myfont    
    global consolefont
    global bigfont   
    global hugefont   
    global preview_img  
    global thumbnail_imgs
    global pe         
    global countdownEnd
    global running
    global state
    global startTime
    global tv_img
    global camera_img

    s = pygame.Surface((1024,768), flags=pygame.SRCALPHA)
    t = time.time()
    camera_end = 300
    screen_start = 675

    #label = myfont.render("time :%.2f"%t, 1, (255,0,0))
    #s.blit(label, (40,40))

    #draw the channel on the bottom
    pygame.draw.rect(s, (16,16,16), pygame.Rect(camera_end, 400, screen_start-camera_end, 50))

    #then draw circles on the channel
    num = 16 
    delta = int(500/num)
    for j in range(4):
        for i in range(num):
            circlex = camera_end - delta - (j*16) + (i*delta) + int((time.time() - startTime) * 50) %delta 
            c = 40+i*((256-40)/num)
            color = (c,c,c)
            #pygame.draw.circle(s, color, (circlex,425), 18, 5)
            bit = consolefont.render("%d"%random.randint(0,1), 1, color)
            s.blit(bit, (circlex, 400 + j*12))

    #then draw the icons
    s.blit(camera_img, (10, 265))
    s.blit(tv_img, (600, 250))

    #then draw the lines
    pygame.draw.line(s, (64,64,64), (camera_end,400), (screen_start,400), 5)
    pygame.draw.line(s, (64,64,64), (camera_end,450), (screen_start,450), 5)
    
    screen.blit(s, (0,0))


def loop():
    global screen
    global myq
    global myfont    
    global consolefont
    global bigfont   
    global hugefont   
    global preview_img  
    global thumbnail_imgs
    global pe         
    global countdownEnd
    global running
    global state
    global startTime
    global tv_img
    global camera_img
    global message

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
            pe.setLed()

        elif item.type == "press":
            state = STATE_COUNTDOWN
            pe.clearLed()
            countdownEnd = time.time() + timer_secs

        elif item.type == "photo":
            if item.name is None:
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
            thumbnail_imgs.append(item.image)
            # no state change.


    ### GENERATE DISPLAY BASED ON STATE ####

    if state == STATE_RESET:
        label = myfont.render("Press button to capture!", 1, (255,255,0))

        lx = 40
        if int(round(time.time()/60))%2 == 0: #even minutes
            ly = 720
            iy0 = 150
            iy1 = 350
        else:
            ly=40
            iy0 = 350
            iy1 = 550

        screen.blit(label, (lx,ly))

        #show last 6 images!
        for i,img in enumerate(thumbnail_imgs):
            if i<3:
                x = 150 + (225 * i)
                y = iy0
            else:
                x = 150 + (225 * (i-3))
                y = iy1

            screen.blit(img, (x,y))

    elif state == STATE_COUNTDOWN:

        timeleft = countdownEnd - time.time() 
        if timeleft <= capture_secs:
            #Start capture n seconds before timer runs out
            registerPhotoEvent(myq)
            state = STATE_CAPTURE

        else:
            #Provide countdown until capture
            label = hugefont.render("%.1f"%timeleft, 1, (0,255,0))
            screen.blit(label, (120,120))

    elif state == STATE_CAPTURE:

        timeleft = countdownEnd - time.time() 
        if timeleft >= 0:
            #Provide countdown until capture
            label = hugefont.render("%.1f"%timeleft, 1, (0,255,0))
            screen.blit(label, (120,120))

        else:
            #Update user w/ status info
            dots = "."*(int(time.time())%3)
            label = myfont.render("Capturing picture%s"%dots, 1, (255,0,255))
            screen.blit(label, (450,450))

    elif state == STATE_TRANSFER:
        #Update user w/ status info
        transferAnimation()
        dots = "."*(int(time.time())%3)
        label = myfont.render("transferring picture%s"%dots, 1, (255,255,0))
        screen.blit(label, (450,450))

    elif state == STATE_PROCESS:
        transferAnimation()
        #Update user w/ status info
        dots = "."*(int(time.time())%3)
        label = myfont.render("processing picture%s"%dots, 1, (0,255,255))
        screen.blit(label, (450,450))

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
                down = 230+(i*20)
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
