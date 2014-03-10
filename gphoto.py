#!/usr/bin/env python

import subprocess
import time

exe = "gphoto2"

def captureAndDownload():
	filename = time.strftime("%y%m%d_%H%M%S.jpg")
	action = "--capture-image-and-download"

	cmd = "%s %s --filename=%s"%(exe, action, filename)

	try:
		output = subprocess.check_output(cmd,
			stderr=subprocess.STDOUT,
			shell=True)

		print output

		return filename

	except subprocess.CalledProcessError as cpe:
		print "%s returned (%d): \"%s\""%(exe, cpe.returncode, cpe.output)

		return None
		

if __name__ == "__main__":

	print captureAndDownload()
