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

    def __init__(self, x=0, y=0, rotacion=0, velocidad=2,aceleracion=1,
                 radio_de_colision=10):
        self.velocidad = velocidad
        grilla = pilas.imagenes.cargar_grilla("sin_imagen.png", 1)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = radio_de_colision
        self.rotacion = rotacion

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

   
        