# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Pacman(Actor):
    """Muestra un personaje similar al juego Pac-Man

    .. image:: ../../pilas/data/manual/imagenes/actores/pacman.png

    Este actor se puede mover con el teclado, pulsando las teclas ``izquierda``,
    ``arriba``, ``abajo`` y ``derecha``.

        >>> pacman = pilas.actores.Pacman(velocidad=5)

    """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.grilla = self.pilas.imagenes.cargar_grilla("pacman.png", 4, 4)
        self.imagen = self.grilla
        self.cuadro = 0
        self.control = self.pilas.escena_actual().control
        self.velocidad = 3
        self.aprender(self.pilas.habilidades.SeMantieneEnPantalla)
        self.radio_de_colision = 5

        self.posicion = 0
        # donde self.posicion puede ser:
        # 0 = para izquierda
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
        """Cambia el cuadro de animación del actor."""
        self.imagen.definir_cuadro(indice)
