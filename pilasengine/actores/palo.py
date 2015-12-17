# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Palo(Actor):

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.imagen = "palo.png"
        self.centro = (0, "centro")

    def actualizar(self):
        pass

    def terminar(self):
        pass