# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento


class Pingu(Actor):
    """Muestra a un pingüino que sabe caminar con el teclado.

    .. image:: ../../pilas/data/manual/imagenes/actores/pingu.png

    Este actor responde al teclado, así que podremos
    usar los direccionales del teclado ``izquierda``, ``arriba``
    y ``derecha``:

        >>> pingu = pilas.actores.Pingu()
    """

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar_grilla("pingu.png", 10)
        self.definir_cuadro(4)
        self.hacer_inmediatamente(Esperando)
        self.radio_de_colision = 30
        self.centro = ("centro", "abajo")
        self.velocidad = 4

    def definir_cuadro(self, indice):
        """Define el cuadro de la animación.

        :param indice: Número de cuadro.
        """
        self.imagen.definir_cuadro(indice)


class Esperando(Comportamiento):
    """Un actor en posición normal o esperando a que el usuario
    pulse alguna tecla.
    """

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(4)
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        if self.control.izquierda:
            self.receptor.hacer_inmediatamente(Caminando)
        elif self.control.derecha:
            self.receptor.hacer_inmediatamente(Caminando)

        if self.control.arriba:
            self.receptor.hacer_inmediatamente(Saltando)


class Caminando(Comportamiento):
    """Representa al personaje caminando por el escenario."""

    def iniciar(self, receptor):
        self.receptor = receptor
        self.cuadros = [5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        self.paso = 0
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        self.avanzar_animacion()

        if self.control.izquierda:
            self.receptor.x -= self.receptor.velocidad
        elif self.control.derecha:
            self.receptor.x += self.receptor.velocidad
        else:
            self.receptor.hacer_inmediatamente(Esperando)

        if self.control.arriba:
            self.receptor.hacer_inmediatamente(Saltando)

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.paso])


class Saltando(Comportamiento):
    """Representa al actor saltando con animación."""

    def iniciar(self, receptor):
        self.dy = 10
        self.receptor = receptor
        self.receptor.definir_cuadro(0)
        self.origen = self.receptor.y
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        self.receptor.y += self.dy
        self.dy -= 0.3

        if self.receptor.y < self.origen:
            self.receptor.y = self.origen
            self.receptor.hacer_inmediatamente(Esperando)

        if self.control.izquierda:
            self.receptor.x -= self.receptor.velocidad
        elif self.control.derecha:
            self.receptor.x += self.receptor.velocidad
