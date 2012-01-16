# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class Camara(object):
    """Representa el punto de vista de la ventana.

    Los atributos ``x`` e ``y`` indican cual debe ser el
    punto central de la pantalla. Por defecto estos
    valores con (0, 0)."""

    def __init__(self, motor):
        self.motor = motor

    @pilas.utils.interpolable
    def _set_x(self, x):
        pilas.eventos.mueve_camara.send("movimiento de camara", x=x, y=self.y, dx=x-self.x, dy=0)
        pilas.mundo.motor.definir_centro_de_la_camara(x, self.y)

    def _get_x(self):
        x, y = pilas.mundo.motor.obtener_centro_de_la_camara()
        return x

    @pilas.utils.interpolable
    def _set_y(self, y):
        eventos.mueve_camara.send("movimiento de camara", x=self.x, y=y, dx=0, dy=y-self.y)
        pilas.mundo.motor.definir_centro_de_la_camara(self.x, y)

    def _get_y(self):
        x, y = pilas.mundo.motor.obtener_centro_de_la_camara()
        return y

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)

