# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor


class Tortuga(Actor):
    "Representa una tortuga que se mueve por la pantalla como la tortuga de Logo."

    def __init__(self, x=0, y=0, dibuja=True):
        if dibuja:
            self.pizarra = pilas.actores.Pizarra()
            self.pizarra.bajar_lapiz()

        self.dibuja = dibuja
        imagen = pilas.imagenes.cargar('tortuga.png')
        Actor.__init__(self, imagen, x=x, y=y)
        self.rotacion = 0

    def avanzar(self, pasos):
        self.hacer_luego(pilas.comportamientos.Avanzar(pasos))

    def giraderecha(self, delta):
        self.hacer_luego(pilas.comportamientos.Girar(delta, 3))

    def giraizquierda(self, delta):
        self.hacer_luego(pilas.comportamientos.Girar(-delta, 3))

    def actualizar(self):
        if self.dibuja:
            self.pizarra.mover_lapiz(self.x, self.y)
