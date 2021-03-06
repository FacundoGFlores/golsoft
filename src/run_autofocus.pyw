#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

from scipy import misc, optimize
import matplotlib.pyplot as plt
import numpy as np

from automask import get_mask
from autofocus import guess_focus_distance
from autopipe import showimage
from dft import get_shifted_dft, get_shifted_idft
from image import imread, normalize, get_intensity, equalize
from pea import get_auto_mask, generic_minimizer, angle2
from pea import get_propagation_array
from ranges import frange
import cache


class Methods(list):
    def __call__(self, func):
        self.append(func)
        return func
methods = Methods()


def get_highpass_mask(shape, radius=0.2, softness=0):
    radius = round(min(shape) * (1 - radius))
    window = np.kaiser(radius, softness)
    mask = 1 - get_mask(shape, window)
    return mask


def get_lowpass_mask(shape, radius=0.2, softness=0):
    radius = round(min(shape) * radius)
    window = np.kaiser(radius, softness)
    mask = get_mask(shape, window)
    return mask

@methods
@cache.hybrid
def get_var(masked_spectrum, distance):
    propagation_array = get_propagation_array(masked_spectrum.shape, distance)
    propagated = propagation_array * masked_spectrum
    reconstructed = get_shifted_idft(propagated)
    module = np.abs(reconstructed)
    fitness = module.var()
    return fitness

@methods
def get_diff_var(masked_spectrum, distance):
    fitness = get_var(masked_spectrum, distance)
    fitness -= get_var(masked_spectrum, -distance)
    return fitness


@methods
@cache.hybrid
def get_int_var(masked_spectrum, distance):
    propagation_array = get_propagation_array(masked_spectrum.shape, distance)
    propagated = propagation_array * masked_spectrum
    reconstructed = get_shifted_idft(propagated)
    intensity = get_intensity(reconstructed)
    fitness = intensity.var()
    return fitness

@methods
def get_diff_int_var(masked_spectrum, distance):
    fitness = get_int_var(masked_spectrum, distance)
    fitness -= get_int_var(masked_spectrum, -distance)
    return fitness


#@methods
@cache.hybrid
def get_lowpass_var(masked_spectrum, distance):
    propagation_array = get_propagation_array(masked_spectrum.shape, distance)
    propagated = propagation_array * masked_spectrum
    lowpass_mask = get_lowpass_mask(propagated.shape, .4)
    propagated = lowpass_mask * propagated
    reconstructed = get_shifted_idft(propagated)
    intensity = get_intensity(reconstructed)
    fitness = intensity.var()
    return fitness

#@methods
def get_diff_lowpass_var(masked_spectrum, distance):
    fitness = get_lowpass_var(masked_spectrum, distance)
    fitness -= get_lowpass_var(masked_spectrum, -distance)
    return fitness



#@methods
@cache.hybrid(reset=0)
def get_highpass_var(masked_spectrum, distance):
    propagation_array = get_propagation_array(masked_spectrum.shape, distance)
    propagated = propagation_array * masked_spectrum
    highpass_mask = get_highpass_mask(propagated.shape, .4)
    propagated = highpass_mask * propagated
    reconstructed = get_shifted_idft(propagated)
    intensity = get_intensity(reconstructed)
    fitness = intensity.var()
    return fitness

#@methods
def get_diff_highpass_var(masked_spectrum, distance):
    fitness = get_highpass_var(masked_spectrum, distance)
    fitness -= get_highpass_var(masked_spectrum, -distance)
    return fitness



#@methods
@cache.hybrid
def get_var_over_hpass_var(*args):
    fitness = get_var(*args) / get_highpass_var(*args)
    return fitness

#@methods
def get_diff_var_over_hpass_var(masked_spectrum, distance):
    fitness = get_var_over_hpass_var(masked_spectrum, distance)
    fitness -= get_var_over_hpass_var(masked_spectrum, -distance)
    return fitness




#@methods
@cache.hybrid
def get_lpass_var_over_hpass_var(*args):
    fitness = get_lowpass_var(*args) / get_highpass_var(*args)
    return fitness


#@methods
def get_diff_lpass_var_over_hpass_var(masked_spectrum, distance):
    fitness = get_lpass_var_over_hpass_var(masked_spectrum, distance)
    fitness -= get_lpass_var_over_hpass_var(masked_spectrum, -distance)
    return fitness


def get_best_contrast_zone(hologram, shape=(256, 256)):
    assert shape[0] <= hologram.shape[0]
    assert shape[1] <= hologram.shape[1]
    rows = hologram.shape[0] - shape[0] + 1
    cols = hologram.shape[1] - shape[1] + 1
    rowsvar = hologram.var(0)
    colsvar = hologram.var(1)
    sumsrowsranges = np.array([rowsvar[top:top + shape[0]].sum()
        for top in xrange(rows)])
    sumscolsranges = np.array([colsvar[left:left + shape[1]].sum()
        for left in xrange(cols)])
    toprow = sumsrowsranges.argmax()
    leftcol = sumscolsranges.argmax()
    print(rows, cols)
    return hologram[toprow:toprow + shape[0], leftcol:leftcol + shape[1]]


def guess_focus_distance(masked_spectrum, extractor):

    def fitness(args):
        return extractor(masked_spectrum, args)

    results = []
    for distance in frange(0, .15, 3):
        xend = generic_minimizer(fitness, distance, [optimize.fmin])
        results.append(xend)
    return results



def main():
    images = [(filename, imread(filename, True))
        for filename in sys.argv[1:]]
    if len(images) < 2:
        if not images:
            lena = misc.imresize(misc.lena(), .5)
            images = [("lena", lena)]

    figure = plt.figure()

    graph_distances = [distance for distance in frange(0.0, 2**-2, 160)]

    for filename, hologram in images:
        print("\nOriginal image: %s" % filename)
        shape = hologram.shape
        showimage(hologram)

        best_zone = get_best_contrast_zone(hologram)
        showimage(best_zone)
        print(best_zone.shape)

        spectrum = get_shifted_dft(hologram)
        mask, masked_spectrum, centered = get_auto_mask(spectrum,
            softness=0, radious_scale=1.5)
        showimage(equalize(centered), equalize(masked_spectrum))

        zone_spectrum = get_shifted_dft(best_zone)
        mask, zone_masked_spectrum, centered = get_auto_mask(zone_spectrum,
            softness=0, radious_scale=1.0)
        showimage(equalize(centered), equalize(zone_masked_spectrum))

        for method in methods:
            print("\nMethod: %s\n" % method.func_name)

            fitness_values = [method(zone_masked_spectrum, distance)
                for distance in graph_distances]
            plt.cla()
            plt.plot(graph_distances, fitness_values, c="blue")

            localmins = guess_focus_distance(zone_masked_spectrum, method)
            fitness = [method(zone_masked_spectrum, dst)
                for dst in localmins]

            plt.scatter(localmins, fitness, c="green")

            bestfitness, globalmin = min(zip(fitness, localmins))
            plt.scatter(globalmin, bestfitness, c="red")

            showimage(figure)
            
            propagation_array = get_propagation_array(zone_spectrum.shape, globalmin)
            propagated = zone_masked_spectrum * propagation_array
            reconstructed = get_shifted_idft(propagated)
            showimage(normalize(np.abs(reconstructed)), 
                normalize(angle2(reconstructed)))
            print(propagated.shape, reconstructed.shape)

            propagation_array = get_propagation_array(shape, globalmin)
            propagated = masked_spectrum * propagation_array
            reconstructed = get_shifted_idft(propagated)
            showimage(normalize(np.abs(reconstructed)), 
                normalize(angle2(reconstructed)))
            print globalmin, "\n"

    return 0


if __name__ == "__main__":
    exit(main())
