#!/usr/bin/env python

import subprocess
import time
import threading
import Queue
import pygame
from events import *
from thumbnail import getThumbnail

exe = "gphoto2"

def getImage(original, resolution, q):

	#print "Thumbing %s"%original
	prvw = getThumbnail(original, resolution)
	if not prvw:
		return None

	return prvw


def disableAutoOff():
	output=""
	cmd = "gphoto2 --set-config /main/settings/autopoweroff=0"
	try:
		output = subprocess.check_output(cmd,
			stderr=subprocess.STDOUT,
			shell=True)

		if -1 == output.lower().find("error"):
			return True

		else:
			print output
			return False

	except subprocess.CalledProcessError as cpe:
		print output
		return False


def captureAndDownload(q):
	filename = time.strftime("%y%m%d_%H%M%S.jpg")
	action = "--capture-image-and-download"
	camera = "--auto-detect"

	#cmd = "%s %s --filename=%s"%(exe, action, filename)
	cmd = [exe, camera, action, "--filename", filename]

	proc = subprocess.Popen(cmd, 
			bufsize=1, 
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)

	#loop over proc while it's alive!
	gotPhoto = False
	while proc.poll() == None:

		#get a line of text from the process, blocking.
		line = proc.stdout.readline()
		print "line in: %s"%line

		#check output strings for 'error'
		if "error" in line.lower():

			#kill the process 
			proc.kill()

			#return the error
			pht = photo( name = None )
			pht.message = line + str(proc.stdout.read()) + str( proc.stderr.read())
			q.put(pht)

			#because of error, we don't want to add any
			#  downloadings to the queue
			return False


		elif "New file" in line:
			gotPhoto = True
			#print "adding downloading"
			q.put(downloading())

	if not gotPhoto: #uh oh - error time

		#return the error
		pht = photo( name = None )
		pht.message = "No image captured - camera might be sleeping or not have been able to focus"
		q.put(pht)

		#because of error, we don't want to add any
		#  downloadings to the queue
		return False
		

	#out of loop? Process has ended. Generate the thumbnails!
	#print "adding photo"
	time.sleep(2)
	q.put(photo(name=filename))

	#when getImage finishes, add a 'preview' event to the queue
	#print "adding preview"
	q.put(preview(pygame.image.load(getImage(filename, (1024,768), q))))

	#continue generating thumbnail in background
	q.put(thumbnail(pygame.image.load(getImage(filename, (200,300), q))))

class photoTaker(threading.Thread):
	def __init__(self, q=None):
		self.q = q
		threading.Thread.__init__(self)
	
	def run(self):
		captureAndDownload(self.q)

def registerPhotoEvent(q):
	mythread = photoTaker(q)
	mythread.start()	#start the waiter
	return mythread


if __name__ == "__main__":

	q = Queue.queue()
	registerPhotoEvent(q)
