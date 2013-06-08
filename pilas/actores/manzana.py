# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor


class Manzana(Actor):
    """Muestra una manzana.

    .. image:: images/actores/manzana.png


    Este actor se podría usar cómo alimento o bonus para otros
    actores.

    """

    def __init__(self, x=0, y=0):
        """ Constructor de la Manzana.

        :param x: Posición horizontal del Actor.
        :type x: int
        :param y: Posición vertical del Actor.
        :type y: int
        """
        imagen = pilas.imagenes.cargar("manzana.png")
        Actor.__init__(self, imagen, x=x, y=y)
        self.radio_de_colision = 50

    def actualizar(self):
        pass