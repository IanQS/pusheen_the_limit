# This line imports the modules we will need. The first is the sys module used
# to read the command line arguments. Second the Python Imaging Library to read
# the image and third numpy, a linear algebra/vector/matrix module.
import sys
from PIL import Image
import os
import numpy as np
np.set_printoptions(threshold=np.inf)
import argparse

# PARAMETERS


BACKGROUND_RATIO = 25 / 100  # looks better on terminal if slight contrast
SQUARE_PCT = 10 / 100  # corner ratio used in determining the background color

# bound below which we know the background is black,
# so we flip the folor
LOWER_BOUND = 25

# Number of acceptable buffer lines on top and bottom as a random Pusheen
# appearing out of nowhere isn't really as visually 'standout'
BUFFER_COUNT = 2


def convert(imgs, debug, remBackground):
    """ Convert the image to ASCII, while dropping the size too

    Args:
       imgs list: list of images to convert
       debug Boolean: whether to print the ASCII to the screen or not
       remBackground Boolean: remove background?

    Returns:
        converted image

    """
    GCF = 0.2
    imStore = []
    chars = ' .,:;irsXA253hMHGS#9B&@'
    chars = chars[::-1]
    chars = np.asarray(list(chars))
    for img_ in imgs:
        img_ = np.asarray(img_)
        img_ = np.array(img_).copy()
        if remBackground:
            img_ = removeBackground(img_)
        img_ -= img_.min()
        img_ = (1.0 - img_ / img_.max())**GCF * (chars.size - 1)

        # Depending on the mode we either store as an image or
        # store as
        ascii_ = "\n".join(("".join(r) for r in chars[img_.astype(int)]))
        imStore.append(ascii_)
        if debug:
            print(ascii_)
            imStore.append(ascii_)
    return imStore


def pareDown(img):
    """Some Pusheen images have a TON of space at the top and bottom
    which is fine for an image, but not fine on my terminal

    Args:
       img : numpy array

    Returns:
        img

    """
    imgList = img.tolist()
    holder = []
    topCount = 0
    bottomCount = 0
    beenInside = False
    for el in imgList:
        if np.std(el) != 0:
            beenInside = True
            holder.append(el)
        else:
            if not beenInside:
                if topCount < BUFFER_COUNT:
                    holder.append(el)
                    topCount += 1
            else:
                if bottomCount < BUFFER_COUNT:
                    holder.append(el)
                    bottomCount += 1
    return np.asarray(holder)


def removeBackground(img):
    """whether to alter the background of the image for sharper ASCII art

    Args:
       img single numpy array of (N, M) (greyscaled)

    Returns:
        altered image

    """

    h, w = img.shape
    lUp = img[h - int(h * SQUARE_PCT):, : int(w * SQUARE_PCT)]
    lBot = img[:int(h * SQUARE_PCT), :int(w * SQUARE_PCT)]
    rUp = img[h - int(h * SQUARE_PCT):, w - int(w * SQUARE_PCT):]
    rBot = img[:int(h * SQUARE_PCT), w - int(w * SQUARE_PCT):]
    background = np.average(lUp + lBot + rUp + rBot)
    sdev = np.std(lUp + lBot + rUp + rBot)
    if background < LOWER_BOUND:
        # is the case where the background is a DARK color
        img[img < LOWER_BOUND] = img.max() * BACKGROUND_RATIO
    else:
        img[img >= (background - sdev)] = img.max() * BACKGROUND_RATIO
    img = pareDown(img)
    return img


def grabImgs(src, shape):
    '''
    Grabs the image(s) from the specified source, resizes them,
    and returns them in a numpy array

    '''
    imStore = []
    if os.path.isdir(src):
        for el in [x for x in os.listdir(src) if not x.endswith('.swp')]:
            img = Image.open(src + '/' + el).convert('L')
            img = img.resize(shape, Image.ANTIALIAS)
            imStore.append(img)
    elif (os.path.isfile(src)):
        imStore.append(Image.open(src))
    else:
        print('Input src was not a directory or a file')
        sys.exit(1)
    return imStore


def pair(arg):
    return [int(x) for x in arg.split(',')]


def parseArgs(args):
    '''
    Parses the args. Just read the docs below they're decent
    '''
    args.add_argument('-sf', '--img-source',
                      help=('File / folder to read from'),
                      default='imgSrc')
    args.add_argument('-sh', '--shape',
                      help=('Tuple of shape to resize image(s) to. Pass in as X,Y e.g 80, 40. I\'ve found that the first value should be about double for the best results'),
                      default=[80, 40],
                      type=pair)
    args.add_argument('-dest', '--destination',
                      help=('File/ folder to save to'),
                      default='imgDest')
    args.add_argument('-db', '--debug',
                      help=('Debug mode'),
                      default=False)
    args.add_argument('-rm', '--remove-background',
                      help=('Remove the background (currently uses sklearn)'),
                      default=True)
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


def saveAsText(textFiles, dest):
    if not os.path.isdir(dest):
        os.mkdir(dest)
    for i, el in enumerate(textFiles):
        fName = dest + '/' + 'git_pusheen_' + str(i) + '.txt'
        with open(fName, 'w+') as f:
            f.write(el)


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
    greyedAndScaled = convert(imgs, flags.debug, flags.remove_background)
    saveAsText(greyedAndScaled, flags.destination)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    main(args)
