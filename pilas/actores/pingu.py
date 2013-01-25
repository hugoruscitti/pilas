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

VELOCIDAD = 4

class Pingu(Actor):
    """Muestra a un pingüino que sabe caminar con el teclado.

    .. image:: images/actores/pingu.png

    Este actor responde al teclado, así que podremos
    usar los direccionales del teclado ``izquierda``, ``arriba``
    y ``derecha``:

        >>> pingu = pilas.actores.Pingu()
    """

    def __init__(self, x=0, y=0):
        """Inicializa al actor.

        :param x: Posición horizontal.
        :param y: Posición vertical.
        """
        Actor.__init__(self, x=x, y=y)
        self.imagen = pilas.imagenes.cargar_grilla("pingu.png", 10)
        self.definir_cuadro(4)
        self.hacer(Esperando())
        self.radio_de_colision = 30
        self.centro = ("centro", "abajo")

    def definir_cuadro(self, indice):
        """Define el cuadro de la animación.

        :param indice: Número de cuadro.
        """
        self.imagen.definir_cuadro(indice)


class Esperando(Comportamiento):
    "Un actor en posicion normal o esperando a que el usuario pulse alguna tecla."

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(4)

    def actualizar(self):
        if pilas.escena_actual().control.izquierda:
            self.receptor.hacer(Caminando())
        elif pilas.escena_actual().control.derecha:
            self.receptor.hacer(Caminando())

        if pilas.escena_actual().control.arriba:
            self.receptor.hacer(Saltando())


class Caminando(Comportamiento):
    """Representa al personaje caminando por el escenario."""

    def iniciar(self, receptor):
        self.receptor = receptor
        self.cuadros = [5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        self.paso = 0

    def actualizar(self):
        self.avanzar_animacion()

        if pilas.escena_actual().control.izquierda:
            self.receptor.x -= VELOCIDAD
        elif pilas.escena_actual().control.derecha:
            self.receptor.x += VELOCIDAD
        else:
            self.receptor.hacer(Esperando())

        if pilas.escena_actual().control.arriba:
            self.receptor.hacer(Saltando())

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

    def actualizar(self):
        self.receptor.y += self.dy
        self.dy -= 0.3

        if self.receptor.y < self.origen:
            self.receptor.y = self.origen
            self.receptor.hacer(Esperando())

        if pilas.escena_actual().control.izquierda:
            self.receptor.x -= VELOCIDAD
        elif pilas.escena_actual().control.derecha:
            self.receptor.x += VELOCIDAD
