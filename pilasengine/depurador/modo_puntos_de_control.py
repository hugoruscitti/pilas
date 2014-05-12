# -*- encoding: utf-8 -*-
from pilasengine.depurador.modo import ModoDepurador


class ModoPuntosDeControl(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        self._dibujar_cruz(painter)

    def _dibujar_cruz(self, painter):
        l = 3

        self._definir_trazo_negro(painter)
        painter.drawLine(-l, -l, l, l)
        painter.drawLine(-l, l, l, -l)

        self._definir_trazo_blanco(painter)
        painter.drawLine(-l, -l, l, l)
        painter.drawLine(-l, l, l, -l)
