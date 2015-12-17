# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.depurador.modo import ModoDepurador
from pilasengine.colores import blanco, negro


class ModoPosicion(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)
        self.ejes = self.pilas.actores.Ejes()

    def cuando_dibuja_actor_sin_transformacion(self, actor, painter):
        self._definir_trazo_blanco(painter)

        x = "{0:0.1f}".format(actor.x)
        y = "{0:0.1f}".format(actor.y)
        texto = "(%s, %s)" % (x, y)

        self._texto(painter, texto, 21, 21, color=negro)
        self._texto(painter, texto, 20, 20, color=blanco)


    def sale_del_modo(self):
        self.ejes.eliminar()