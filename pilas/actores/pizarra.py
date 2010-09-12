# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
from PySFML import sf
import pilas

class Pizarra(Actor):

    def __init__(self):
        self.imagen = sf.Image(640, 480)
        self.imagen.CreateMaskFromColor(sf.Color.Black)

        Actor.__init__(self, self.imagen)

    def dibujar_punto(self, x, y, color=sf.Color.Red):
        self.imagen.SetPixel(320 + x, 240 - y, color)

    def dibujar_cuadrado(self, x, y, ancho=8, color=sf.Color.Black):
        inicio_x = x - ancho/2
        fin_x = x + ancho/2

        inicio_y = y - ancho/2
        fin_y = y + ancho/2

        for i in range(inicio_x, fin_x):
            for j in range(inicio_y, fin_y):
                self.dibujar_punto(i, j, color)

