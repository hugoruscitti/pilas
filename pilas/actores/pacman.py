# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class Pacman(Actor):
    """Muestra un personaje similar al juego Pac-Man

    .. image:: images/actores/pingu.png

    Este actor se puede mover con el teclado, pulsando las teclas ``izquierda``,
    ``arriba``, ``abajo`` y ``derecha``.

        >>> pacman = pilas.actores.Pacman(velocidad=5)
    """

    def __init__(self, x=0, y=0, velocidad=3):
        self.grilla = pilas.imagenes.cargar_grilla("pacman.png", 4, 4)
        Actor.__init__(self, self.grilla, x, y)
        self.cuadro = 0
        self.control = pilas.escena_actual().control
        self.velocidad = velocidad
        self.posicion = 0  # 0 = para izquierda
                           # 1 = para la derecha
                           # 2 = para arriba
                           # 3 = para abajo

    def actualizar(self):
        if self.control.izquierda:
            self.posicion = 0
            self.x -= self.velocidad
            self._reproducir_animacion()
        elif self.control.derecha:
            self.posicion = 1
            self.x += self.velocidad
            self._reproducir_animacion()
        elif self.control.abajo:
            self.posicion = 3
            self.y -= self.velocidad
            self._reproducir_animacion()
        elif self.control.arriba:
            self.posicion = 2
            self.y += self.velocidad
            self._reproducir_animacion()

    def _reproducir_animacion(self):
        self.cuadro += 0.4

        if self.cuadro > 3:
            self.cuadro = 0

        self.definir_cuadro(int(self.posicion * 4 + self.cuadro))

    def definir_cuadro(self, indice):
        self.imagen.definir_cuadro(indice)
