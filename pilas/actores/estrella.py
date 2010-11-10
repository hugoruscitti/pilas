# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas


class Estrella(Actor):
    "Representa una estrella de color amarillo."

    def __init__(self, x=0, y=0):
        imagen = pilas.imagenes.cargar('estrella.png')
        Actor.__init__(self, imagen, x=x, y=y)
        self.rotacion = 0
