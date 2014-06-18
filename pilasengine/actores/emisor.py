# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
import random

class Emisor(Actor):
    """
    """

    def iniciar(self):
        self.imagen = self.pilas.imagenes.cargar_grilla("invisible.png")
        self.imagen_particula = self.pilas.imagenes.cargar_grilla("particula.png")
        self.cantidad_maxima_particulas = 10
        self.contador = 0
        self.fundir = True
        self.constante = True

        self.dx_min = -1
        self.dx_max = 1

        self.dy_min = -1
        self.dy_max = 1

    def actualizar(self):
        if self.constante:
            self.crear_particula()
            self.contador += 1
        else:
            if self.contador <= self.cantidad_maxima_particulas:
                self.crear_particula()
                self.contador += 1

    def crear_particula(self):
        dx = self.rango(self.dx_min, self.dx_max) / 5.0
        dy = self.rango(self.dy_min, self.dy_max) / 5.0

        self.pilas.actores.Particula(self.x, self.y,
                                     dx=dx, dy=dy,
                                     imagen=self.imagen_particula)

    def rango(self, minimo, maximo):
        if minimo < maximo:
            return random.randint(minimo, maximo)
        else:
            return minimo