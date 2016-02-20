#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Flores Facundo
# Año: 2016
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Estado: Produccion

from ConfigParser import ConfigParser

from traits.api import Bool, Str, Color, Float, Int, List
from traits.api import HasTraits, Button, File, Range, Enum, Instance, Dict
from traitsui.api import View, Item, Group, HSplit, VSplit, HGroup, VGroup
from traitsui.api import Handler

from ..controllers.datainput import DatainputHandler

CAM_PATH = "data/cameras.ini"
WAV_PATH = "data/wavelengths.ini"


class Datainput_model(HasTraits):
    """ ModelView para el manejo de datos de los hologramas:
        1- Imagenes
        2- Camara
        3- Wavelength Predefinidos
    """
    # Datos
    imagecolor = Color("(0,0,0)")
    imagewavelength = Int(0)
    wavelength_nm = Range(
        400., 750., 650.,
        mode="xslider",
        enter_set=True,
        auto_set=False
    )
    # Files
    holo_filename = File()
    ref_filename = File()
    obj_filename = File()
    # Botones
    btn_update_hologram = Button("Actualizar holograma")
    btn_load_parameters = Button("Cargar")
    btn_save_parameters = Button("Guardar")
    # Groups
    grp_datainput = Group(
        Item('holo_filename', label="Hologram"),
        Item('obj_filename', label="Object"),
        Item('ref_filename', label="Reference"),
        Item("btn_update_hologram", show_label=False),
        HGroup(
            Item(
                "imagecolor",
                style='readonly',
                label="Dominant color"
            ),
            Item(
                "imagewavelength",
                style="readonly",
                label="Dominant wavelength"
            ),
        ),
        HGroup(
            Item(
                "btn_save_parameters",
                label="Parametros"
            ),
            Item(
                "btn_load_parameters",
                show_label=False
            )
        ),
        label="Input file",
        show_border=True,
    )

    datainput_view = View(
        grp_datainput,
        handler=DatainputHandler
    )


if __name__ == '__main__':
    m = DataInput_Model()
    m.configure_traits()
