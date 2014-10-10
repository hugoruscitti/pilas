# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento



class Shaolin(Actor):
    """Representa un luchador que se puede controlar con el teclado,
    puede saltar, golpear y recibir golpes."""

    def iniciar(self, x=0, y=0):
        self._cargar_animaciones()
        self.hacer(Parado)

    def _cargar_animaciones(self):
        self.animaciones = {
            "parado": self.pilas.imagenes.cargar_grilla("shaolin/parado.png", 4, 1),
        }

    def cambiar_animacion(self, nombre):
        """Cambia la animación del Cooperativista.

        :param nombre: El nombre de la animación que se quiere mostar.
        """
        self.imagen = self.animaciones[nombre]
        self.centro = ("centro", "abajo")

class Parado(Comportamiento):

    def iniciar(self, receptor):
        """Inicializa el comportamiento.

        :param receptor: La referencia al actor.
        """
        self.receptor = receptor
        self.receptor.cambiar_animacion("parado")
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        self.receptor.imagen.avanzar(10)
        pass
