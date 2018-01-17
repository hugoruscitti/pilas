# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from PyQt4 import QtCore
from pilasengine.depurador.modo import ModoDepurador


class ModoRadiosDeColision(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        pass

    def _dibujar_circulo(self, painter, x, y, radio):
        self._definir_trazo_negro(painter)
        painter.drawEllipse(-radio, -radio, radio*2, radio*2)

        self._definir_trazo_blanco(painter)
        painter.drawEllipse(-radio, -radio, radio*2, radio*2)
