# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Zanahoria(Actor):
    """Representa un actor que parece una Zanahoria."""

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.cuadro_normal = self.pilas.imagenes.cargar("zanahoria_normal.png")
        self.cuadro_reir = self.pilas.imagenes.cargar("zanahoria_sonrie.png")

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
        self.hacer(self.pilas.comportamientos.Saltar,
                   cuando_termina=self.normal)

    def decir(self, mensaje):
        """Emite un mensaje usando un globo similar al de los commics.

        :param mensaje: La cadena de mensaje que mostrará."""
        self.sonreir()
        Actor.decir(self, mensaje)
        self.pilas.tareas.una_vez(2, self.normal)
