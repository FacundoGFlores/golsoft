#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Flores Facundo
# Año: 2016
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Estado: Produccion
import os
from ConfigParser import ConfigParser

from traits.api import Enum
from traitsui.api import Handler

CAM_PATH = 'data/cameras.ini'
WAV_PATH = 'data/wavelengths.ini'


class ExtradataHandler(Handler):
    """ Controlador para el ModelView: Extradata
    """
    def object_camera_changed(self, info):
        print info.object.camera

    def load_cameras(self):
        cp = ConfigParser()
        try:
            with open(CAM_PATH) as cam_file:
                cp.readfp(cam_file)
        except IOError:
            print "Error leyendo el archivo de camaras"
        cameras = {}
        for section in cp.sections():
            cameras[section] = dict(cp.items(section))
        if cameras:
            return Enum(cameras.keys(), label="Camera")
        else:
            return Enum("No hay camaras disponibles", label="Camera")

    def load_wavelengths(self):
        cp = ConfigParser()
        try:
            with open(WAV_PATH) as cam_file:
                cp.readfp(cam_file)
        except IOError:
            print "Error leyendo el archivo de wavelengths"
        wavelengths = dict(cp.items("Wavelengths"))
        if wavelengths:
            wavelengths = ["Custom"] + [
                "%s - %s" % (w, k) for k, w in wavelengths.items()]
            return Enum(wavelengths, label="Wavelength")
        else:
            return Enum("No hay wavelengths disponibles", label="Wavelengths")
