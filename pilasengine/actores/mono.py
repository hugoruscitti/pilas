# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PyQt4 import QtGui
from pilasengine.actores.actor import Actor


class Mono(Actor):

    def iniciar(self):
        self.imagen = "mono.png"
        self.sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        self.radio_de_colision = 50

    def actualizar(self):
        pass

    def saltar(self):
        self.sonido.reproducir()