# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilasengine
from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento

class Alien(Actor):
    """Representa un personaje de juego tipo RPG."""

    def pre_iniciar(self):
        self.imagen = "alien.png"
        
    def dar_vuelta(self):
        self.rotacion = [360]
        
    def actualizar(self):
        if self.pilas.control.izquierda:
            self.x -= 5
            self.espejado = True
        if self.pilas.control.derecha:
            self.x += 5
            self.espejado = False
        if self.pilas.control.arriba:
            self.y += 5
        if self.pilas.control.abajo:
            self.y -= 5                        

