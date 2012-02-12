#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from autopipe import red
import Image
import numpy as np
import sys
import ImageOps

def logscale(image):
    array = np.asarray(image, dtype=float)
    array -= array.min()
    array *= np.expm1(1) / array.max()
    array = np.log1p(array)
    array *= 255
    image = Image.fromarray(array.astype('uint8'))
    return image

def toLmode(image):
    image = image.convert("F")
    array = np.asarray(image, dtype=float)
    array -= array.min()
    array *= 255 / array.max()
    image = Image.fromarray(array.astype('uint8'))
    return image


def equalizefloat(image):
    array = np.asarray(image)
    shape = array.shape
    array = array.flatten()
    sorters = array.argsort()
    for order, place in enumerate(sorters):
        array[place] = order
    array *= 255. / order
    array = array.reshape(shape)
    image = Image.fromarray(array.astype("uint8"))
    return image


def equalize(image):
    if image.mode in ("F"):
        return equalizefloat(image)
    else:
        return ImageOps.equalize(image)

def autocontrast(image):
    if image.mode in ("F"):
        image = toLmode(image)
    try:
        return ImageOps.autocontrast(image)
    except IOError:
        red("Error on '%s' image" % image.mode)


def main():
    image = Image.open(sys.argv[1])
    width, height = image.size
    if max(width, height) > 600:
        print "Resizing..."
        prop = max(width, height) / 600.
        image = image.resize((int(width / prop), int(height / prop)), 1)

    print("Original image:")
    autopipe.showimage(image)

    print("With logscale:")
    autopipe.showimage(logscale(image))

    print("With auto-contrast:")
    autopipe.showimage(autocontrast(image))

    print("With equalized histogram:")
    autopipe.showimage(equalize(image))

if __name__ == "__main__":
    exit(main())
