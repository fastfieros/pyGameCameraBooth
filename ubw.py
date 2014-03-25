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
    sleep = 0.1

    button_source_port = 'B' #??
    button_source_pin = '2'  #??

    button_read_port = 'B'   #??
    button_read_pin = '3'    #??

    button_led_port = 'A'    #??
    button_led_pin = '0'     #??

    output = '0'
    input = '1' 

    on = '1'
    off = '0'

	kill=False

	def __init__(self, q=None, flag=None):

        self.writelock = threading.Lock()
        self.setup_button_source_0 = "PD,%s,%s,%s\r\n"%(
                self.button_source_port,
                self.button_source_pin,
                self.output)

        self.setup_button_source_1 = "PO,%s,%s,%s\r\n"%(
                self.button_source_port,
                self.button_source_pin,
                self.on)

        self.setup_button_read = "PD,%s,%s,%s\r\n"%(
                self.button_read_port,
                self.button_read_pin,
                self.input)

        self.setup_button_led = "PD,%s,%s,%s\r\n"%(
                self.button_led_port,
                self.button_led_pin,
                self.output)


        self.probe_button_state = "PI,%s,%s\r\n"%(
                self.button_read_port,
                self.button_read_pin)

        self.match_button_state = "PI,%s,\r\n"%(self.off)


		self.flag = flag

		self.ser = serial.Serial(port=self.DEVICE, 
			    baudrate=9600,
			    bytesize=8,
			    parity=serial.PARITY_NONE,
			    stopbits=serial.STOPBITS_ONE,
			    timeout=5 )

        self.send(self.setup_button_source_0)
        self.send(self.setup_button_source_1)
        self.send(self.setup_button_read)
        self.send(self.setup_button_led)

		self.q = q
		threading.Thread.__init__(self)

    def send(data):
        #Don't write data while background tasks are writing data..
        self.writelock.acquire()
        self.ser.write(data)
        self.writelock.release()


    def setLed():
        button_led_set = "PO,%s,%s,%s\r\n"%(self.button_led_port, self.button_led_pin,self.on)
        self.send(button_led_set)

    def clearLed():
        button_led_set = "PO,%s,%s,%s\r\n"%(self.button_led_port, self.button_led_pin,self.off)
        self.send(button_led_set)

    def dimLed(value):

        freq = "120"
        freqCMD = "F,%s,%s,%s\r\n"%(freq,
                self.button_led_port,
                self.button_led_pin)

        self.send(freqCMD)


	def checkPin(self):
		self.send(self.probe_button_state)

		try:
			line = self.ser.readline()
			return line == self.match_button_state

		except serial.SerialTimeoutException as ste:
			return False	

	def waitForPin(self):

		while True != self.checkPin():
			if self.kill:
				self.cleanup()
				return None

			time.sleep(self.sleep)
		
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


