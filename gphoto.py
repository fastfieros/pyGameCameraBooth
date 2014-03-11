#!/usr/bin/env python

import subprocess
import time
import threading
import Queue

exe = "gphoto2"

def captureAndDownload():
	filename = time.strftime("%y%m%d_%H%M%S.jpg")
	action = "--capture-image-and-download"

	cmd = "%s %s --filename=%s"%(exe, action, filename)

	try:
		output = subprocess.check_output(cmd,
			stderr=subprocess.STDOUT,
			shell=True)


		print "(gphoto) captured: \"%s\""%(filename)
		return filename

	except subprocess.CalledProcessError as cpe:
		print "%s returned (%d): \"%s\""%(exe, cpe.returncode, cpe.output)

		return None
		
class photo():
	type = "photo"
	name = None

class photoTaker(threading.Thread):
	def __init__(self, q=None):
		self.q = q
		threading.Thread.__init__(self)
	
	def run(self):
	
		p = photo()
		p.name = captureAndDownload()

		if self.q:
			self.q.put(p)

def registerPhotoEvent(q=None):
	mythread = photoTaker(q)
	mythread.start()    #start the waiter
	return mythread


if __name__ == "__main__":

	#print captureAndDownload()
	registerPhotoEvent()
