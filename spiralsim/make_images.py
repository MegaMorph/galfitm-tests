#!/usr/bin/env python

# Note that this should be used with original GALFIT.

from glob import glob
import pyfits
import sys, os

def make_images():

    noiselevels = [1, 5, 10, 50, 100]
    noise = [pyfits.getdata('n%i.fits'%i) for i in noiselevels]

    gals = glob('galfit.gal*')

    for g in gals:
        os.system('galfitm-0.0.3 %s'%g)
        imgname = g.replace('galfit.', '')
        for i, n in enumerate(noiselevels):
            img = pyfits.open(imgname+'.fits')
            img[0].data += noise[i]
            img.writeto(imgname+'n%i.fits'%n, clobber=True)

if __name__ =='__main__':
    sys.exit(make_images())

