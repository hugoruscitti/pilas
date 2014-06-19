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

        self.escala_min = 0.1
        self.escala_max = 2

        self.rotacion_min = 0
        self.rotacion_max = 0

        self.transparencia_min = 0
        self.transparencia_max = 0

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
        d_escala = self.rango(self.escala_min, self.escala_max)
        d_rotacion = self.rango(self.rotacion_min, self.rotacion_max)
        d_transparencia = self.rango(self.transparencia_min, self.transparencia_max)

        p = self.pilas.actores.Particula(self.x, self.y,
                            dx=dx, dy=dy,
                            imagen=self.imagen_particula)

        p.transparencia = d_transparencia
        p.escala = d_escala
        p.rotacion = d_rotacion


    def rango(self, minimo, maximo):
        if minimo < maximo:
            return self.rand_float_range(minimo, maximo)
        else:
            return minimo

    def rand_float_range(self, start, end):
        return random.random() * (end - start) + start