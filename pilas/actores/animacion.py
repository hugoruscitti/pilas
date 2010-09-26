# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
from pilas.comportamientos import Comportamiento
import copy

VELOCIDAD = 4


class Animacion(Actor):
    """Representa una animacion de una grilla de imagenes.

    Este actor toma una grilla de cuadros de animacion
    y los reproduce hasta que la animacion termina. Cuando
    la animacion termina se elimina a si mismo.
    """

    def __init__(self, grilla, ciclica=False):
        Actor.__init__(self)
        self.animacion = copy.copy(grilla)
        self.definir_cuadro(0)
        self.tick = 0
        self.ciclica = ciclica     # Indica si la animacion debe seguir existiendo.

    def definir_cuadro(self, indice):
        self.animacion.definir_cuadro(indice)
        self.animacion.asignar(self)


    def actualizar(self):
        if self.tick > VELOCIDAD:
            self.tick = 0
            ha_reiniciado = self.animacion.avanzar()
            self.animacion.asignar(self)

            # Si la animacion ha terminado se elimina de la pantalla.
            if ha_reiniciado and not self.ciclica:
                self.eliminar()
        else:
            self.tick += 1
