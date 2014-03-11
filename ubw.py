#!/usr/bin/env python
import os,time
import threading
import serial
import Queue
from events import *

class flag():
	def __init__(self, init=True):
		self.value = init

	def done(self):
		self.value = False

	def go(self):
		return self.value

class ubw(threading.Thread):

	DEVICE = "/dev/ttyACM0"
	PROBE  = "PI,C,2\r"
	MATCH  = "PI,0\r\n"

	def __init__(self, q=None, flag=None):

		self.sleep = 0.1
		self.flag = flag

		self.ser = serial.Serial(port=self.DEVICE, 
			    baudrate=9600,
			    bytesize=8,
			    parity=serial.PARITY_NONE,
			    stopbits=serial.STOPBITS_ONE,
			    timeout=5 )

		self.q = q
		threading.Thread.__init__(self)

	def checkPin(self):
		self.ser.write(self.PROBE)

		try:
			line = self.ser.readline()
			return line == self.MATCH

		except serial.SerialTimeoutException as ste:
			return False	

	def waitForPin(self):

		while True != self.checkPin():
			time.sleep(self.sleep)
		
		print "(ubw) Button Pressed!"

		if self.q:
			self.q.put(press())

	def run(self):
		if self.flag: #if a flag is defined, loop until it is set
			while self.flag.go():
				self.waitForPin()	

		else: #otherwise it's a one-shot
			self.waitForPin()	


	def cleanup(self):
		self.ser.close()

	def __del__(self):
		self.cleanup()


def registerPinEvent(q, flag=None):
	mythread = ubw(q, flag)
	mythread.start()    #start the waiter
	return mythread


if __name__ == "__main__":

	#u = ubw(None, None)
	#u.waitForPin()
	myq = Queue.Queue()
	myf = None
	t = registerPinEvent(myq, myf)

	print myq.get()

	#myf.done()


