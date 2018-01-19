# This line imports the modules we will need. The first is the sys module used
# to read the command line arguments. Second the Python Imaging Library to read
# the image and third numpy, a linear algebra/vector/matrix module.
import sys
from PIL import Image
import os
import numpy as np
import argparse

def grabImgs(src, shape):
    '''
    Grabs the image(s) from the specified source, resizes them,
    and returns them in a numpy array

    Not using a numpy array or whatever
    '''
    imStore = []
    if os.path.isdir(src):
        for el in [x for x in os.listdir(src) if not x.endswith('.swp')]:
            img = Image.open(src + '/' + el)
            img = img.resize(shape, Image.ANTIALIAS)
            imStore.append(img)
    elif (os.path.isfile(src)):
        imStore.append(Image.open(src))
    else:
        print('Input src was not a directory or a file')
        sys.exit(1)
    return imStore


def parseArgs(args):
    args.add_argument('-sf', '--img-source',
                      help=('File / folder to read from'),
                      default='imgSrc')
    args.add_argument('-s', '--shape',
                      help=('Tuple of shape to resize image(s) to'),
                      default=(200, 200))
    args.add_argument('-d', '--destination',
                      help=('File/ folder to save to'),
                      default='imgDest')
    args.add_argument('-db', '--debug',
                      help=('Debug mode'),
                      default=False)
    return args.parse_args()


def saveIntermediate(imgs, saveTo, prefix):
    if not os.path.isdir(saveTo):
        os.mkdir(saveTo)
    for i, el in enumerate(imgs):
        el.save(saveTo + "/" + prefix + '_img' + str(i) + '.png', "PNG")


def main(args):
    '''
    1) Grab the folder / file and resize everything
    2) (debug) save to an intermediate folder
    3) ascii conversion
    '''
    flags = parseArgs(args)

    imgs = grabImgs(flags.img_source, flags.shape)
    if flags.debug:
        saveIntermediate(imgs, '.debugImgs', 'postResize')

    chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    sys.exit(main(args))
