# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.deslizador_horizontal import DeslizadorHorizontal
from pilasengine import colores


class ManejadorPropiedad(DeslizadorHorizontal):

    def pre_iniciar(self, x=0, y=0, actor='actor', propiedad='x', _min=0, _max=100):
        pass

    def iniciar(self, x=0, y=0, actor='actor', propiedad='x', _min=0, _max=100):
        valor_inicial = getattr(actor, propiedad)
        DeslizadorHorizontal.iniciar(self, x, y, _min, _max, propiedad, valor_inicial=valor_inicial)
        self.actor = actor
        self.propiedad = propiedad
        self.conectar(self.cuando_cambia)

    def cuando_cambia(self, valor):
        setattr(self.actor, self.propiedad, valor)
