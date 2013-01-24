# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class Zanahoria(Actor):
    """Representa un actor que parece una Zanahoria."""

    def __init__(self, x=0, y=0):
        """Inicializa el actor en una posición inicial.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        """
        self.cuadro_normal = pilas.imagenes.cargar("zanahoria_normal.png")
        self.cuadro_reir = pilas.imagenes.cargar("zanahoria_sonrie.png")

        Actor.__init__(self, x=x, y=y)
        self.normal()
        self.radio_de_colision = 25

    def normal(self):
        """Cambia la imagen actual por una donde se ve la zanahora normal."""
        self.imagen = self.cuadro_normal
        self.centro = ('centro', 65)

    def sonreir(self):
        """Cambia la imagen actual por una en donde tiene una sonrisa"""
        self.imagen = self.cuadro_reir
        self.centro = ('centro', 65)

    def saltar(self):
        """Realiza un salto hacia arriba."""
        self.sonreir()
        accion = pilas.comportamientos.Saltar(cuando_termina=self.normal)
        self.hacer(accion)

    def decir(self, mensaje):
        """Emite un mensaje usando un globo similar al de los commics.

        :param mensaje: La cadena de mensaje que mostrará."""
        self.sonreir()
        Actor.decir(self, mensaje)
        pilas.mundo.agregar_tarea_una_vez(1, self.normal)
