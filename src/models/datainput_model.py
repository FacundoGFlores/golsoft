#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Flores Facundo
# Año: 2016
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Estado: Produccion

from traits.api import HasTraits, Button, File
from traitsui.api import View, Item, Group
from traitsui.api import Handler

from ..controllers.datainput import DatainputHandler


class Datainput_model(HasTraits):
    """ ModelView para el manejo de datos de los hologramas:
        Archivos de imagenes.
    """
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
        Item('holo_filename', label="Holograma"),
        Item('obj_filename', label="Objecto"),
        Item('ref_filename', label="Referencia"),
        Item("btn_update_hologram", show_label=False),
        label="Archivos de Entrada",
        show_border=True,
    )

    view_datainput = View(
        grp_datainput,
        handler=DatainputHandler
    )

if __name__ == '__main__':
    m = DataInput_Model()
    m.configure_traits()
