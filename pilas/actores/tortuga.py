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
        self.pizarra = pilas.actores.Pizarra()

        if dibuja:
            self.bajalapiz()
        else:
            self.subelapiz()

        imagen = pilas.imagenes.cargar('tortuga.png')
        Actor.__init__(self, imagen, x=x, y=y)
        self.rotacion = 0

    def avanzar(self, pasos):
        self.hacer_luego(pilas.comportamientos.Avanzar(pasos))

    def giraderecha(self, delta):
        self.hacer_luego(pilas.comportamientos.Girar(abs(delta), 3))

    def giraizquierda(self, delta):
        self.hacer_luego(pilas.comportamientos.Girar(-abs(delta), 3))

    def actualizar(self):
        self.pizarra.mover_lapiz(self.x, self.y)

    def bajalapiz(self):
        self.pizarra.bajar_lapiz()

    def subelapiz(self):
        self.pizarra.levantar_lapiz()

    def pon_color(self, color):
        self.hacer_luego(pilas.comportamientos.CambiarColor(color))

    # Alias de metodos
    av = avanzar
    gd = giraderecha
    gi = giraizquierda
    bl = bajalapiz
    sl = subelapiz
    pc = pon_color


    def get_color(self):
        return self.pizarra.color

    def set_color(self, color):
        self.pizarra.definir_color(color)

    color = property(get_color, set_color)
