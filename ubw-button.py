#!/usr/bin/env python
import serial

DEVICE = "/dev/ttyACM0"
PROBE  = "PI,C,2\r"
MATCH  = "PI,0\r\n"

ser = serial.Serial(port=DEVICE, 
		    baudrate=9600,
                    bytesize=8,
		    parity=serial.PARITY_NONE,
                    stopbits=STOPBITS_ONE,
                    timeout=5 )



if __name__ == "__main__":
	print "HAY"
