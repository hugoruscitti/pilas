# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from PyQt4 import QtGui


class Particula(Actor):

    def __init__(self, pilas, x, y, dx, dy, imagen):
        Actor.__init__(self, pilas, x, y)
        self.imagen = imagen
        self.dx = dx
        self.dy = dy

        #self.composicion = 12 # Aditivo
        #self.composicion = 0 # CompositionMode_Plus
        self.composicion = 12 # CompositionMode_Plus

    def actualizar(self):
        self.x += self.dx
        self.y += self.dy
        self.escala -= 0.01
        self.transparencia += 1.3
        self.rotacion += 0.1

        if self.escala < 0.1:
            self.eliminar()
