#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Flores Facundo
# Año: 2016
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Estado: Produccion

from ConfigParser import ConfigParser

from traits.api import Color, HasTraits, Int, Instance, Range
from traitsui.api import Group, HGroup, Handler, Item, View

from ..controllers.extradata import ExtradataHandler


class Extradata_model(HasTraits):
    """ ModelView para el manejo de datos extra de los hologramas:
        Camaras y Wavelength
    """
    hnd_extra = ExtradataHandler()
    camera = hnd_extra.load_cameras()
    wavelength = hnd_extra.load_wavelengths()
    wavelength_nm = Range(400., 750., 650., mode="xslider", enter_set=True,
        auto_set=False)
    imagecolor = Color("(0,0,0)")
    imagewavelength = Int(0)

    grp_extradata = Group(
        "camera",
        HGroup(
            Item("imagecolor", style='readonly', label="Color Dominante"),
            Item("imagewavelength", style="readonly",
                label="Wavelength dominante"),
        ),
        "wavelength",
        "wavelength_nm"
    )

    view_extradata = View(
        grp_extradata,
        handler=ExtradataHandler
    )

if __name__ == '__main__':
    e = Extradata_model()
    e.configure_traits()
