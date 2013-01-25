#!/usr/bin/env python

# Note that this should be used with original GALFIT.

from glob import glob
import pyfits
import os, sys, getopt


"""make_images.py - Create images for galfitm spiralsim test

    Usage:
        make_images.py [arch]
        
        where [arch] is 'linux' or 'osx',
        defaulting to linux if not specified.

"""

def make_images(arch='linux'):

    noiselevels = [1, 5, 10, 50, 100]
    noise = [pyfits.getdata('n%i.fits'%i) for i in noiselevels]

    gals = glob('galfit.gal*')

    for g in gals:
        os.system('galfitm-0.0.3-%s %s'%(arch, g))
        imgname = g.replace('galfit.', '')
        for i, n in enumerate(noiselevels):
            img = pyfits.open(imgname+'.fits')
            img[0].data += noise[i]
            img.writeto(imgname+'n%i.fits'%n, clobber=True)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hf", ["help", "force"])
        except getopt.error, msg:
            raise Usage(msg)
        clobber = False
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 1
            if o in ("-f", "--force"):
                clobber = True
        if len(args) == 0:
            arch = 'linux'
        if len(args) == 1:
            arch = args[0]
        elif len(args) > 1:
            raise Usage("Wrong number of arguments")
        make_images(arch)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2
 
if __name__ == "__main__":
    sys.exit(main())
