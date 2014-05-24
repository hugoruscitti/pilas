# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import math

from pilasengine import comportamientos


class Proyectil(comportamientos.Comportamiento):
    "Hace que un actor se comporte como un proyectil."

    def iniciar(self, receptor, velocidad_maxima=5, aceleracion=1,
                angulo_de_movimiento=90, gravedad=0):
        """Construye el comportamiento.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param aceleracion: Valor entre 0 y 1 para indicar lo rápido que
                            acelerará el actor.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor.
        :param gravedad: La velocidad vertical con la que caerá el actor.

        """
        super(Proyectil, self).iniciar(receptor)
        self._velocidad_maxima = velocidad_maxima
        self._aceleracion = aceleracion
        self._angulo_de_movimiento = angulo_de_movimiento
        self._gravedad = gravedad
        self._vy = self._gravedad

        if (self._aceleracion == 1):
            self._velocidad = self._velocidad_maxima
        else:
            self._velocidad = 0

    def actualizar(self):
        self._velocidad += self._aceleracion

        if self._velocidad > self._velocidad_maxima:
            self._velocidad = self._velocidad_maxima

        self.mover_respecto_angulo_movimiento()

    def mover_respecto_angulo_movimiento(self):
        """Mueve el actor hacia adelante respecto a su angulo de movimiento."""
        rotacion_en_radianes = math.radians(self._angulo_de_movimiento)
        dx = math.cos(rotacion_en_radianes) * self._velocidad
        dy = math.sin(rotacion_en_radianes) * self._velocidad
        self.receptor.x += dx

        if self._gravedad > 0:
            self.receptor.y += dy + self._vy
            self._vy -= 0.1
        else:
            self.receptor.y += dy