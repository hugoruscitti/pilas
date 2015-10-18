# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Manzana(Actor):
    """Muestra una manzana.

    .. image:: ../../pilas/data/manual/imagenes/actores/manzana.png

    Este actor se podría usar cómo alimento o bonus para otros
    actores.
    """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar("manzana.png")
        self.radio_de_colision = 50
