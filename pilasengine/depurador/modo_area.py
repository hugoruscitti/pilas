# -*- encoding: utf-8 -*-
from pilasengine.depurador.modo import ModoDepurador


class ModoArea(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        self._dibujar_rectangulo(painter, actor)

    def _dibujar_rectangulo(self, painter, actor):
        (dx, dy) = actor.centro
        ancho = actor.ancho
        alto = actor.alto

        self._definir_trazo_negro(painter)
        painter.drawRect(-dx, -dy, ancho, alto)

        self._definir_trazo_blanco(painter)
        painter.drawRect(-dx, -dy, ancho, alto)