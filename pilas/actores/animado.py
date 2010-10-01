# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
import copy

class Animado(Actor):
    """Representa un actor que tiene asociada una grilla con cuadros de animacion.

    Una de las variantes que introduce este actor es el
    método 'definir_cuadro', que facilita la animación de personajes.
    """

    def __init__(self, grilla):
        Actor.__init__(self)
        self.animacion = copy.copy(grilla)
        self.definir_cuadro(0)

    def definir_cuadro(self, indice):
        self.animacion.definir_cuadro(indice)
        self.animacion.asignar(self)
