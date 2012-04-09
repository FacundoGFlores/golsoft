#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This is a simple implementation of the Fourier-Mellin Trasform
image = [m, n]
ft_magnitude = |fft(image)|
lp_ft_magnitude = logpolar(ft_magnitude)
fmt = fft(lp_ft_magnitude)
"""

from autopipe import showimage
from image import imread, equalize
from scipy import misc
from pea import guess_director_angles, get_ref_beam
from fmt import get_shiftedfft
import sys



def main():
    images = [(filename, imread(filename, True)) for filename in sys.argv[1:]]
    if len(images) < 2:
        if not images:
            lena = misc.imresize(misc.lena(), .5)
            images = [("lena", lena)]

    for filename, image in images:
        print("Original image: %s" % filename)
        alpha, beta = guess_director_angles(image)
        print alpha, beta
        ref_beam = get_ref_beam(image.shape, alpha, beta)
        showimage(equalize(image), equalize(ref_beam.real))
        image_fft = equalize(get_shiftedfft(image))
        ref_beam_fft = equalize(get_shiftedfft(ref_beam.real))
#        showimage(image_fft, ref_beam_fft)

    return 0


if __name__ == "__main__":
    exit(main())