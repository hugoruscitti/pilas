# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas


class Pelota(Actor):
    "Representa una pelota de Volley."

    def __init__(self):
        imagen = pilas.imagenes.cargar('pelota.png')
        Actor.__init__(self, imagen)
        self.rotacion = 0
