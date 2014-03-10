#!/usr/bin/env python

import os,sys
import Image

suffix = ".tmp.jpg"

def getThumbnail(infile, size=(800,600)):
	outfile = os.path.splitext(infile)[0] + ".tmb"

	if os.path.isfile(outfile):
		return outfile

	try:
		im = Image.open(infile)
		im.thumbnail(size)
		im.save(outfile, "JPEG")

	except IOError:
		print "Error making tumbnail.."

	return outfile
