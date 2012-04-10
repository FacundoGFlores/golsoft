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
from image import imread, equalize, normalize
from scipy import misc
from pea import guess_director_angles, get_ref_beam
from dft import get_shifted_dft
import sys



def main():
    images = [(filename, imread(filename, True)) for filename in sys.argv[1:]]
    if len(images) < 2:
        if not images:
            lena = misc.imresize(misc.lena(), .5)
            images = [("lena", lena)]

    for filename, image in images:
        print("Original image: %s" % filename)
        image = normalize(image)
        alpha, beta = guess_director_angles(image)
        print alpha, beta
        ref_beam = get_ref_beam(image.shape, alpha, beta)
        showimage(equalize(image), equalize(ref_beam.real))

        image_dft = equalize(get_shifted_dft(image))
        ref_beam_dft = normalize(get_shifted_dft(ref_beam.real))
        showimage(image_dft, ref_beam_dft)

    return 0


if __name__ == "__main__":
    exit(main())
