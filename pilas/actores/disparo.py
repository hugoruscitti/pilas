# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion
import math

class Disparo(Animacion):
    "Representa un disparo que avanza."

    def __init__(self, grilla="sin_imagen.png", frames=1, x=0, y=0, rotacion=0,
                 velocidad_maxima=1, aceleracion=1, radio_de_colision=10,
                 angulo_de_movimiento=90):
        grilla = pilas.imagenes.cargar_grilla(grilla, frames)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = radio_de_colision
        self.rotacion = rotacion
        self.velocidad_maxima = velocidad_maxima
        self.velocidad = 0
        self.aceleracion = aceleracion
        self.radio_de_colision = radio_de_colision
        self.angulo_de_movimiento = angulo_de_movimiento

    def actualizar(self):
        Animacion.actualizar(self)
        self.avanzar()

    def avanzar(self):
        "Hace avanzar la nave en direccion a su angulo."
        rotacion_en_radianes = math.radians(-self.rotacion + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy

class Misil(Disparo):

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=7,aceleracion=0.1,
                 angulo_de_movimiento=90):

        Disparo.__init__(self,
                         grilla="disparos/misil.png",
                         frames=3,
                         x=x,
                         y=y,
                         rotacion=rotacion,
                         velocidad_maxima=velocidad_maxima,
                         aceleracion=aceleracion,
                         radio_de_colision=15,
                         angulo_de_movimiento=angulo_de_movimiento)

    def avanzar(self):
        self.velocidad += self.aceleracion

        if self.velocidad > self.velocidad_maxima:
            self.velocidad = self.velocidad_maxima

        rotacion_en_radianes = math.radians(-self.angulo_de_movimiento + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy
