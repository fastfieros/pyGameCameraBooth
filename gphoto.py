#!/usr/bin/env python

import subprocess
import time
import threading
import Queue
from events import *

exe = "gphoto2"

###TODO move downloading to events.py
class downloading(event):
    type="downloading"
    progress=0

    def __init__(self, progress=0)
        self.progress=progress

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
    camera = "--auto-detect"

	#cmd = "%s %s --filename=%s"%(exe, action, filename)
	cmd = [exe, camera, action, "--filename", filename]

    proc = subprocess.Popen(cmd, 
            bufsize=1, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    #loop over proc while it's alive!
    while proc.poll() == None:

        #get a line of text from the process, blocking.
        line = proc.stdout.readline()

        #check output strings for 'error'
		if "error" in line.lower():

            #kill the process 
            proc.kill()

            #return the error
		    self.q.put( photo(
                name = None,
                message = line + str(proc.stdout.read()) + str( proc.stderr.read())
                )

            #because of error, we don't want to add any
            #  downloadings to the queue
            return


		elif "downloading" in line.lower():
		    self.q.put(photo(name=filename))
		    self.q.put(downloading(progress=0))

    #out of loop? Process has ended
    self.q.put(downloading(progress=1))


class photoTaker(threading.Thread):
	def __init__(self, q=None):
		self.q = q
		threading.Thread.__init__(self)
	
	def run(self):
	
		captureAndDownload()

def registerPhotoEvent(q):
	mythread = photoTaker(q)
	mythread.start()    #start the waiter
	return mythread


if __name__ == "__main__":

    q = Queue.queue()
	registerPhotoEvent(q)
