# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animado
import copy

VELOCIDAD = 10


class Animacion(Animado):
    """Representa una animacion de una grilla de imagenes.

    Este actor toma una grilla de cuadros de animacion
    y los reproduce hasta que la animacion termina. Cuando
    la animacion termina se elimina a si mismo.

    El constructor tiene algunos parámetros de utilidad:

        - El parámetro ``ciclica`` permite hacer animaciones infinitas, que se repiten siempre, por defecto vale ``False`` que significa que la animación terminará y no se repetirá.  
        - El parámetro ``velocidad`` tiene que ser un número que indicará la cantidad de cuadros por segundo que se tienen que mostrar en la animación.

        Por ejemplo, para mostrar una explosión infinita podrías
        escribir:

        >>> grilla = pilas.imagenes.cargar_grilla("explosion.png", 7)
        >>> animacion = pilas.actores.Animacion(grilla, ciclica=True, velocidad=1)

        .. image:: images/actores/explosion.png
    """

    def __init__(self, grilla, ciclica=False, x=0, y=0, velocidad=VELOCIDAD):
        Animado.__init__(self, grilla, x=x, y=y)
        self.tick = 0
        self.ciclica = ciclica
        self.definir_velocidad_de_animacion(velocidad)

    def definir_velocidad_de_animacion(self, velocidad_de_animacion):
        self._velocidad_de_animacion = (1000.0 / 60) * velocidad_de_animacion

    def obtener_velocidad_de_animacion(self):
        return self._velocidad_de_animacion

    velocidad_de_animacion = property(obtener_velocidad_de_animacion, definir_velocidad_de_animacion, doc="Es la cantidad de cuadros por segundo a mostrar")

    def actualizar(self):
        self.tick += self.velocidad_de_animacion

        if self.tick > 1000.0:
            self.tick -= 1000.0
            ha_reiniciado = self.imagen.avanzar()

            # Si la animacion ha terminado se elimina de la pantalla.
            if ha_reiniciado and not self.ciclica:
                self.eliminar()
