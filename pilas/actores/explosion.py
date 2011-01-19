# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion

class Explosion(Animacion):
    "Representa una explosion para una bomba, dinamita etc..."

    def __init__(self, x=0, y=0):
        Animacion.__init__(self, pilas.imagenes.Grilla("explosion.png", 7), x=x, y=y)
        self.sonido_explosion = pilas.sonidos.cargar("explosion.wav")
        self.sonido_explosion.reproducir()
