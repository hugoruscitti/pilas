# -*- encoding: utf-8 -*-
from pilasengine.depurador.modo import ModoDepurador
from pilasengine.colores import blanco


class ModoPosicion(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        self._definir_trazo_blanco(painter)

        x = "{0:0.1f}".format(actor.x)
        y = "{0:0.1f}".format(actor.y)
        texto = "(%s, %s)" %(x, y)

        escala_x, escala_y = actor.escala_x, actor.escala_y

        if actor._espejado:
            escala_x *= -1

        #painter.scale(1 -escala_x, 1-escala_y)
        painter.rotate(actor.rotacion)

        self._texto(painter, texto, 20, 20, color=blanco)

        #painter.scale(escala_x, escala_y)
        painter.rotate(-actor.rotacion)