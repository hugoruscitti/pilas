# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilasengine
from pilasengine.actores.maton import Maton
from pilasengine.comportamientos.comportamiento import Comportamiento

class Calvo(Maton):
    """Representa un personaje de juego tipo RPG."""

    def iniciar(self, x=0, y=0):
        self.imagen = self.pilas.imagenes.cargar_grilla("rpg/calvo.png", 3, 4)
