#!/usr/bin/env python

import os,sys
import Image

def getThumbnail(infile, size=(800,600)):
	outfile = os.path.splitext(infile)[0] + ("_%dX%d.jpg"%(size[0], size[1]))

	if os.path.isfile(outfile):
		return outfile

	try:
		im = Image.open(infile)
		im.thumbnail(size)
		im.save(outfile, "JPEG")

	except IOError:
		print "Error making tumbnail.."

	return outfile
