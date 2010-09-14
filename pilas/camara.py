# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from PySFML import sf


class Camara(object):
    """Representa el punto de vista de la ventana.

    Los atributos ``x`` e ``y`` indican cual debe ser el
    punto central de la pantalla. Por defecto estos
    valores con (0, 0)."""

    def __init__(self, app):
        self.view = app.GetDefaultView()

    def _set_x(self, x):
        if pilas.utils.es_interpolacion(x):
            x.apply(self, function='_set_x')
        else:
            self.view.SetCenter(x, self.y)

    def _get_x(self):
        x, y = self.view.GetCenter()
        return x

    def _set_y(self, y):
        if pilas.utils.es_interpolacion(y):
            y.apply(self, function='_set_y')
        else:
            self.view.SetCenter(self.x, -y)

    def _get_y(self):
        x, y = self.view.GetCenter()
        return y

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)

