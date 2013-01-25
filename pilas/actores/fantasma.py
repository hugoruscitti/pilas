# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class Fantasma(Actor):
    """Muestra un fantasma similar al del juego Pac-Man

    .. image:: images/actores/fantasma.png

    Este actor se puede mover con el teclado, pulsando las teclas ``izquierda``,
    ``arriba``, ``abajo`` y ``derecha``.

        >>> pacman = pilas.actores.Pacman(velocidad=5)
    """

    def __init__(self, x=0, y=0, velocidad=3):
        """ Constructor del Fantasma

        :param x: Posición horizontal de la explosion.
        :type x: int
        :param y: Posición vertical de la explosion.
        :type y: int
        :param velocidad: Velocidad con la que se desplaza el fantasma.
        :type velocidad: int
        """
        self.grilla = pilas.imagenes.cargar_grilla("fantasma.png", 8, 1)
        Actor.__init__(self, self.grilla, x, y)
        self.cuadro = 0
        self.control = pilas.escena_actual().control
        self.velocidad = velocidad
        self.posicion = 0  # 0 = para arriba
                           # 1 = para abajo
                           # 2 = para izquierda
                           # 3 = para derecha

    def actualizar(self):
        if self.control.izquierda:
            self.posicion = 2
            self.x -= self.velocidad
            self._reproducir_animacion()
        elif self.control.derecha:
            self.posicion = 3
            self.x += self.velocidad
            self._reproducir_animacion()
        elif self.control.abajo:
            self.posicion = 1
            self.y -= self.velocidad
            self._reproducir_animacion()
        elif self.control.arriba:
            self.posicion = 0
            self.y += self.velocidad
            self._reproducir_animacion()

    def _reproducir_animacion(self):
        self.cuadro += 0.2

        if self.cuadro > 1:
            self.cuadro = 0

        self.definir_cuadro(int(self.posicion * 2 + self.cuadro))

    def definir_cuadro(self, indice):
        """Cambia el cuadro de animación a mostrar.

        :param indice: Número de cuadro a mostrar.
        """
        self.imagen.definir_cuadro(indice)
