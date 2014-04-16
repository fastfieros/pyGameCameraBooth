#!/usr/bin/env python

import os
import Image
from random import randint

def getThumbnail(infile, size=(800,600)):

    #outfile = os.path.splitext(infile)[0] + ("_%dX%d.jpg"%(size[0], size[1]))
    outfile = os.path.splitext(infile)[0] + ("_%dX%d.png"%(size[0], size[1]))

    if os.path.isfile(outfile):
        return outfile

    try:
        s0 = int(round(.9*size[0]))
        s1 = int(round(.9*size[1]))
        os.system("convert %s -thumbnail %dx%d -unsharp 2x1.0+0.5+0.1 -bordercolor snow -background \"#222222\" +polaroid %s"%(infile, s0, s1, outfile))
        #im = Image.open(infile)
        #im.thumbnail(size)
        #im.save(outfile, "JPEG")

    except IOError:
        print "Error making tumbnail.."

    return outfile
