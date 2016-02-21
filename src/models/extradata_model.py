#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Flores Facundo
# Año: 2016
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Estado: Produccion

from ConfigParser import ConfigParser

from traits.api import HasTraits, Instance
from traitsui.api import Group, View, Handler

from ..controllers.extradata import ExtradataHandler


class Extradata_model(HasTraits):
    """ ModelView para el manejo de datos extra de los hologramas:
        Camaras y Wavelength
    """
    hnd_extra = ExtradataHandler()
    camera = hnd_extra.load_cameras()

    grp_extradata = Group(
        "camera"
    )

    view_extradata = View(
        grp_extradata,
        handler=ExtradataHandler
    )

if __name__ == '__main__':
    e = Extradata_model()
    e.configure_traits()
