#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from autopipe import showimage, red, blue
from enhance import equalize, autocontrast, logscale
from itertools import combinations
from scipy.ndimage import geometric_transform, gaussian_filter
from scipy.ndimage import maximum_filter1d, minimum_filter1d
import Image as pil
import numpy as np
import os
import sys

tau = np.pi * 2

def get_maxmins(array, window=25):
    mins = minimum_filter1d(array, window)
    maxmins = maximum_filter1d(mins, window)
    return maxmins

def get_minmaxs(array, window=25):
    maxs = maximum_filter1d(array, window)
    minmaxs = minimum_filter1d(maxs, window)
    return minmaxs


def get_peaks1d(array, count=1, window=30):
    ddiffs = np.diff(array)
    minmaxs = get_minmaxs(ddiffs, window)
    three_minmaxs = np.array([center
        for center in minmaxs.argsort()[-count:]])
    three_minmaxs.sort()

    maxmins = get_maxmins(ddiffs, window)
    three_maxmins = np.array([center - 1
        for center in maxmins.argsort()[:count]])
    three_maxmins.sort()
    midpoints = ((three_minmaxs + three_maxmins) / 2.).round()

    refineds = [array[center - 5:center + 5].argsort()[-1] + center - 5
        for center in midpoints]
    return refineds


def graf(*data):
    for datum in data:
        pylab.plot(datum)
    return pylab.show()


def get_segment(array, startpoint, endpoint):
    startingx, startingy = startpoint
    endingx, endingy = endpoint
    xtravel = endingx - startingx
    ytravel = endingy - startingy
    totaltravel = (xtravel ** 2 + ytravel ** 2) ** .5

    def out2in(hipotenusa):
        xfrom = startingx + xtravel * hipotenusa / totaltravel
        yfrom = startingy + ytravel * hipotenusa / totaltravel
        return xfrom, yfrom

    segment = geometric_transform(array, out2in, (totaltravel,), order=3)
    return segment


def get_circles(array, count=3, window=30):
    xsums = np.array([array[:, x].sum() for x in range(array.shape[1])])
    xpeaks = get_peaks1d(xsums, count)
    ysums = np.array([array[y, :].sum() for y in range(array.shape[0])])
    ypeaks = get_peaks1d(ysums, count)

    assert sum(np.diff(xpeaks)) >= sum(np.diff(ypeaks)) #lo extendemos luego
    
    centers = []
    for xpeak in xpeaks:
        ysums = np.array([array[y, xpeak - 5:xpeak + 5].sum()
            for y in range(array.shape[0])])
        ypeak = get_peaks1d(ysums)[0]
        centers.append((int(xpeak), int(ypeak)))

    print centers
    circles = [] #value, center, radio
    valley = xsums[centers[0][0]:centers[1][0]]
    radius = int(get_peaks1d(-valley, 1)[0])
    circles.append((array[centers[0]], centers[0], radius))
    valley = xsums[centers[1][0]:centers[2][0]]
    radius = int(centers[2][0] - centers[1][0] - get_peaks1d(-valley, 1)[0])
    circles.append((array[centers[2]], centers[2], radius))

    return circles


def draw_circle(canvas_shape, center, radius, fill=1):
    xc, yc = center
    r = radius
    array = np.ndarray(canvas_shape)
    Yiter, Xiter = np.ogrid[0:canvas_shape[0] , 0:canvas_shape[1]]
    mask = (Xiter - xc) ** 2 + (Yiter - yc) ** 2 <= r ** 2
    array[mask] = fill
    return array

def radial_extrusion(array, center=None):
    inshape = array.shape
    assert len(inshape) == 1
    center = center or inshape[0] / 2.
    outxs = max(inshape[0] - center, center) * 2
    outys = outxs

    def out2in((outx, outy)):
        rho = ((outx-center) ** 2 + (outy-center) ** 2) ** .5
        if outy > center:
            return (center + rho, )
        else:
            return (center - rho, )

    extrusion = geometric_transform(array, out2in, (outxs, outys))
    return extrusion


def main():

    window = np.hanning(500)
    window2d = radial_extrusion(window)
    equalized = window2d * 255
    showimage(pil.fromarray(equalized))

    window = np.bartlett(500)
    window2d = radial_extrusion(window)
    equalized = window2d * 255
    showimage(pil.fromarray(equalized))

    window = np.blackman(500)
    window2d = radial_extrusion(window)
    equalized = window2d * 255
    showimage(pil.fromarray(equalized))

    window = np.hamming(500)
    window2d = radial_extrusion(window)
    equalized = window2d * 255
    showimage(pil.fromarray(equalized))

    window = np.kaiser(500, 14) #https://en.wikipedia.org/wiki/Kaiser_window
    window2d = radial_extrusion(window)
    equalized = window2d * 255
    showimage(pil.fromarray(equalized))


#    for filename in sys.argv[1:]:
#        image = pil.open(filename)
#        array = np.array(image)
#        if "." in filename:
#            filename = "".join(filename.split(".")[:-1])
#        circles = sorted((get_circles(array)))
#        for number, (value, center, radius) in enumerate(circles):
#            print number, value, center, radius
#            mask = draw_circle(array.shape, center, radius)
#            masked = np.float32(array * mask)
#            mask = np.float32(mask)
#            mask_name = '%s-%d-mask.tiff' % (filename, number)
#            image = pil.fromarray(mask)
#            image.save(mask_name)
#            masked_name = '%s-%d-masked.tiff' % (filename, number)
#            image = pil.fromarray(masked)
#            image.save(masked_name)


if __name__ == "__main__":
    exit(main())
