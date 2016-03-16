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

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar_grilla("invisible.png")
        self.imagen_particula = self.pilas.imagenes.cargar_grilla("particula.png")

        self._contador_frecuencia_creacion = 0
        self.frecuencia_creacion = 0.1
        self.particulas_vivas = 0

        self.constante = True
        self.vida = 1

        self.dx_min = -2
        self.dx_max = 2

        self.dy_min = -2
        self.dy_max = 2

        self.escala_min = 1
        self.escala_max = 1

        self.rotacion_min = 0
        self.rotacion_max = 0

        self.transparencia_min = 0
        self.transparencia_max = 0

        self.x_min = 0
        self.x_max = 0

        self.y_min = 0
        self.y_max = 0

        self.escala_fin_min = 1
        self.escala_fin_max = 1

        self.transparencia_fin_min = 100
        self.transparencia_fin_max = 100

        self.rotacion_fin_min = 0
        self.rotacion_fin_max = 0

        self.aceleracion_x_min = 0
        self.aceleracion_x_max = 0

        self.aceleracion_y_min = 0
        self.aceleracion_y_max = 0
        self.z = 0

    def definir_composicion(self, valor):
        if valor in [0, 'normal', None]:
            self._composicion = 0
        elif valor in [1, 'blanco']:
            self._composicion = 12
        elif valor in [2, 'negro']:
            self._composicion = 8
        else:
            raise Exception("Modo de composicion no permitido: ." + valor)

    def obtener_composicion(self):
        return self._composicion

    composicion = property(obtener_composicion, definir_composicion)


    def actualizar(self):
        self._contador_frecuencia_creacion += 0.016  # 1/60 segundos

        if self._contador_frecuencia_creacion > self.frecuencia_creacion:
            self._contador_frecuencia_creacion -= self.frecuencia_creacion
            self.crear_particula()

    def crear_particula(self):
        dx = self.rango(self.dx_min, self.dx_max) / 5.0
        dy = self.rango(self.dy_min, self.dy_max) / 5.0
        d_escala = self.rango(self.escala_min, self.escala_max)
        d_rotacion = self.rango(self.rotacion_min, self.rotacion_max)
        d_transparencia = self.rango(self.transparencia_min, self.transparencia_max)
        d_x = self.rango(self.x_min, self.x_max)
        d_y = self.rango(self.y_min, self.y_max)

        p = self.pilas.actores.Particula(self,
                                         self.x + d_x, self.y + d_y,
                                         dx=dx, dy=dy,
                                         imagen=self.imagen_particula,
                                         vida=self.vida)

        p.transparencia = d_transparencia
        p.escala = d_escala
        p.rotacion = d_rotacion
        p.composicion = self._composicion

        p.escala_fin = self.rango(self.escala_fin_min, self.escala_fin_max)
        p.transparencia_fin = self.rango(self.transparencia_fin_min, self.transparencia_fin_max)
        p.rotacion_fin = self.rango(self.rotacion_fin_min, self.rotacion_fin_max)

        p.aceleracion_x = self.rango(self.aceleracion_x_min, self.aceleracion_x_max)
        p.aceleracion_y = self.rango(self.aceleracion_y_min, self.aceleracion_y_max)


        self.particulas_vivas += 1


    def rango(self, minimo, maximo):
        if minimo < maximo:
            return self.rand_float_range(minimo, maximo)
        else:
            return minimo

    def rand_float_range(self, start, end):
        return random.random() * (end - start) + start

    def se_elimina_particula(self, particula):
        self.particulas_vivas -= 1
