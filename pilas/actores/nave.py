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

class Nave(Animacion):
    "Representa una nave que puede disparar."

    def __init__(self, x=0, y=0, velocidad=2):
        self.velocidad = velocidad
        grilla = pilas.imagenes.Grilla("nave.png", 2)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = 20
        self.aprender(pilas.habilidades.PuedeExplotar)
        self.contador_frecuencia_disparo = 0

    def actualizar(self):
        Animacion.actualizar(self)

        if pilas.mundo.control.izquierda:
            self.rotacion += self.velocidad
        elif pilas.mundo.control.derecha:
            self.rotacion -= self.velocidad

        if pilas.mundo.control.arriba:
            self.avanzar()

        self.contador_frecuencia_disparo += 1

        if pilas.mundo.control.boton:
            if self.contador_frecuencia_disparo > 10:
                self.contador_frecuencia_disparo = 0
                self.disparar()

    def disparar(self):
        "Hace que la nave dispare."
        pilas.actores.Disparo(self.x, self.y, self.rotacion, 4)

    def avanzar(self):
        "Hace avanzar la nave en direccion a su angulo."
        rotacion_en_radianes = math.radians(self.rotacion + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy
