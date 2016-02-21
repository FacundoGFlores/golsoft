#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Flores Facundo
# Año: 2016
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Estado: Produccion

from traits.api import HasTraits, Str, Range, Enum, Bool, Instance
from traitsui.api import Item, Group, View, Handler, Label

from src.models.datainput_model import Datainput_model


class Golapp(HasTraits):
    """ Aplicacion principal, la cual incorpora las diferentes vistas
        definidas dentro de los modelos.
    """
    datainput = Instance(Datainput_model)

    grp_datainput = Group(
        Group(
            Item(name='datainput', style='custom'),
            show_labels=False
        ),
        label='Datos de Entrada',
        show_border=True
    )
    view = View(
        grp_datainput,
        title='Golsoft App v2',
        resizable=True,
    )

if __name__ == '__main__':
    golapp = Golapp(datainput=Datainput_model())
    golapp.configure_traits()
