# -*- encoding: utf-8 -*-
from pilasengine.depurador.modo import ModoDepurador
from pilasengine.colores import blanco


class ModoPuntosDeControl(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        self._definir_trazo_negro(painter)
        painter.drawLine(-3, -3, 3, 3)
        painter.drawLine(-3, 3, 3, -3)

        self._definir_trazo_blanco(painter)
        painter.drawLine(-3, -3, 3, 3)
        painter.drawLine(-3, 3, 3, -3)