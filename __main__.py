# This line imports the modules we will need. The first is the sys module used
# to read the command line arguments. Second the Python Imaging Library to read
# the image and third numpy, a linear algebra/vector/matrix module.
import sys
from PIL import Image
import os
import numpy as np
import argparse


def convert(imgs, debug):
    GCF = 0.2
    imStore = []
    chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\\\"^`'. "
    chars = np.asarray(list(chars))
    for img_ in imgs:
        img_ = np.asarray(img_)
        try:
            img_ -= img_.min()
        except ValueError:
            img_ = np.array(img_).copy()
        img_ = (1.0 - img_ / img_.max())**GCF * (chars.size - 1)

        # Depending on the mode we either store as an image or
        # store as
        if not debug:
            ascii_ = "\n".join(("".join(r) for r in chars[img_.astype(int)]))
            print(ascii_)
            imStore.append(ascii_)
        else:
            img_ = Image.fromarray(img_)
            if img_.mode != 'RGB':
                img_ = img_.convert('RGB')
            imStore.append(img_)
    return imStore


def removeBackground(img):
    from skimage import filters
    from scipy import ndimage as ndi
    from skimage import morphology
    pass




def grabImgs(src, shape, remBackground):
    '''
    Grabs the image(s) from the specified source, resizes them,
    and returns them in a numpy array

    Not using a numpy array or whatever
    '''
    imStore = []
    if os.path.isdir(src):
        for el in [x for x in os.listdir(src) if not x.endswith('.swp')]:
            img = Image.open(src + '/' + el).convert('L')
            if remBackground:
                img = removeBackground(img)
            img = img.resize(shape, Image.ANTIALIAS)
            imStore.append(img)
    elif (os.path.isfile(src)):
        imStore.append(Image.open(src))
    else:
        print('Input src was not a directory or a file')
        sys.exit(1)
    return imStore


def parseArgs(args):
    '''
    Parses the args. Just read the docs below they're decent
    '''
    args.add_argument('-sf', '--img-source',
                      help=('File / folder to read from'),
                      default='imgSrc')
    args.add_argument('-sh', '--shape',
                      help=('Tuple of shape to resize image(s) to'),
                      default=(75, 40))
    args.add_argument('-dest', '--destination',
                      help=('File/ folder to save to'),
                      default='imgDest')
    args.add_argument('-db', '--debug',
                      help=('Debug mode'),
                      default=False)
    args.add_argument('-rm', '--remove-background',
                      help=('Remove the background (currently uses sklearn)'),
                      default=False)
    return args.parse_args()


def saveIntermediate(imgs, saveTo, prefix):
    '''
    Save the intermediate values. useful for debugging.

    imgs: list
        list of images to be saved

    saveTo: string
        directory for data to be saved to. Created if doesn't exist

    prefix: string
        prefix to append to image name so that we can inspect at different
        stages
    '''
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

    imgs = grabImgs(flags.img_source, flags.shape, flags.remove_background)
    if flags.debug:
        saveIntermediate(imgs, '.debugImgs', 'postResize')
    greyedAndScaled = convert(imgs, flags.debug)
    if flags.debug:
        saveIntermediate(greyedAndScaled, '.debugImgs', 'greyed')
        sys.exit(0)
    else:
        pass


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    main(args)
