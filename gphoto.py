#!/usr/bin/env python

import subprocess
import time
import threading
import Queue
from events import *

exe = "gphoto2"

def disableAutoOff():
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


def captureAndDownload(p):
	filename = time.strftime("%y%m%d_%H%M%S.jpg")
	action = "--capture-image-and-download"

	cmd = "%s %s --filename=%s"%(exe, action, filename)

	try:
		output = subprocess.check_output(cmd,
			stderr=subprocess.STDOUT,
			shell=True)


		#print "(gphoto) output\n@@@@@@@\n%s\n@@@@@@@\n\n"%(output)

		if -1 == output.lower().find("error"):

			#print "(gphoto) captured: \"%s\""%(filename)
			p.name = filename

		else:
			p.name = None
			p.message = "%s returned: \"%s\""%(exe, output)

	except subprocess.CalledProcessError as cpe:
		print "%s returned (%d): \"%s\""%(exe, cpe.returncode, cpe.output)

		p.name = None
 		p.message = "%s returned (%d): \"%s\""%(exe, cpe.returncode, cpe.output)

class photoTaker(threading.Thread):
	def __init__(self, q=None):
		self.q = q
		threading.Thread.__init__(self)
	
	def run(self):
	
		p = photo()
		captureAndDownload(p)

		if self.q:
			self.q.put(p)

def registerPhotoEvent(q=None):
	mythread = photoTaker(q)
	mythread.start()    #start the waiter
	return mythread


if __name__ == "__main__":

	#print captureAndDownload()
	registerPhotoEvent()
