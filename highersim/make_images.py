#!/usr/bin/env python

# Note that this should be used with original GALFIT.

from glob import glob
from astropy.io import fits as pyfits
import os, sys, getopt


"""make_images.py - Create images for galfitm spiralsim test

    As well as creating singe-band images from the model feedmes, this
    routine produces multi-band model feedmes and corresponding
    images.  It also produces fit feedmes for the various noise levels
    and non-parametric versions.

    Usage:
        make_images.py [arch]
        
        where [arch] is 'linux' or 'osx',
        defaulting to linux if not specified.

        Run from each folder, e.g. spiral, bending, etc.

"""

#noiselevels = [1, 5, 10, 50, 100]
#nonparams = [False, True]

noiselevels = [1]
nonparams = [False]

def make_images(arch='linux'):
    noise = [pyfits.getdata('../n%i.fits'%i) for i in noiselevels]

    gals = glob('galfit.gal*')
    for g in gals:
        make_mwl_model_feedme(g)

    gals = glob('galfit.gal*')
    for g in gals:
        os.system('galfitm-0.0.3-%s %s'%(arch, g))
        imgname = g.replace('galfit.', '')
        for i, n in enumerate(noiselevels):
            img = pyfits.open(imgname+'.fits')
            img[0].data += noise[i]
            img.writeto(imgname+'n%i.fits'%n, clobber=True)

    feedmes = glob('feedme.gal*[0123456789]')
    for f in feedmes:
        make_mwl_fit_feedme(f)

    feedmes = glob('feedme.gal*[0123456789]')
    feedmes += glob('feedme.gal*[0123456789]mwl')
    for f in feedmes:
        make_noise_feedme(f)


def make_noise_feedme(feedme):
    feedmelines = open(feedme).readlines()
    for i, n in enumerate(noiselevels):
        for nonparam in nonparams:
            if nonparam:
                np = 'n'
            else:
                np = ''
            feedmeout = open(feedme+'n%i%s'%(n,np), 'w')
            for l in feedmelines:
                ls = l.split(None, 2)
                if len(ls) > 1 and ls[0] == 'A)':
                    l = l.replace('.fits', 'n%i.fits'%n)
                if len(ls) > 1 and ls[0] == 'B)':
                    l = l.replace('fit.fits', 'n%i%sfit.fits'%(n,np))
                if nonparam and len(ls) > 1 and ls[0] == 'U)':
                    l = l.replace('0', '1', 1)
                feedmeout.write(l)
        feedmeout.close()


def make_mwl_model_feedme(feedme='galfit.gal8'):
    bands = 'ugrizYJHK'
    # corresponds to bulge or disk in illustration model B:
    mag_disk = [17.687,16.717,15.753,15.315,15.019,14.936,14.745,14.425,14.299]
    # corresponds to bulge in illustration model E:
    mag_spheroid = [18.546,17.519,15.753,15.084,14.764,14.623,14.433,14.02,13.78]
    # corresponds to disk in illustration model E:
    mag_arms = [16.999,16.127,15.753,15.529,15.389,15.41,15.384,15.192,15.281]

    component = 0
    feedmelines = open(feedme).readlines()
    for i, b in enumerate(bands):
        feedmeout = open(feedme+b, 'w')
        for l in feedmelines:
            ls = l.split(None, 2)
            if len(ls) > 1 and ls[0] == '3)':
                component += 1
                mag0 = float(ls[1])
                if component == 1:
                    magmwl = mag_spheroid
                elif component == 2:
                    magmwl = mag_disk
                else:
                    magmwl = mag_arms
                deltamag = magmwl[2] - mag0
                mag = magmwl[i] - deltamag
                mags = '%.3f'%mag
                l = l.replace(ls[1], mags)
            if len(ls) > 1 and ls[0] == 'B)':
                l = l.replace('.fits', b+'.fits')
            feedmeout.write(l)
        feedmeout.close()
                

def make_mwl_fit_feedme(feedme='feedme.gal8'):
    bands = 'ugrizYJHK'
    feedmelines = open(feedme).readlines()
    feedmeout = open(feedme+'mwl', 'w')
    for l in feedmelines:
        ls = l.split(None, 3)
        if len(ls) > 1 and ls[0] == '3)':
            l = l.replace(' 1 ', ' 7 ')
        if len(ls) > 1 and ls[0] == 'A)':
            out = ','.join(ls[1].replace('.fits', b+'.fits') for b in bands)
            l = l.replace(ls[1], out)
            l += 'A1) u,g,r,i,z,Y,J,H,K                                # Band labels\n'
            l += 'A2) 3543,4770,6231,7625,9134,10305,12483,16313,22010 # Band wavelengths\n'
        if len(ls) > 1 and ls[0] == 'B)':
            l = l.replace('fit.fits', 'mwlfit.fits')
        if len(ls) > 1 and ls[0][0] in 'DJ':
            l = l.replace(ls[1], ','.join([ls[1]]*9))
        feedmeout.write(l)
    feedmeout.close()


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hf", ["help", "force"])
        except getopt.error as msg:
            raise Usage(msg)
        clobber = False
        for o, a in opts:
            if o in ("-h", "--help"):
                print(__doc__)
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
    except Usage as err:
        print(err.msg, file=sys.stderr)
        print("For help use --help", file=sys.stderr)
        return 2
 
if __name__ == "__main__":
    sys.exit(main())
