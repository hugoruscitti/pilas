# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas


class Estrella(Actor):
    """Representa una estrella de color amarillo.

        .. image:: images/actores/estrella.png

    """

    def __init__(self, x=0, y=0):
        """ Constructor de la Estrella

        :param x: Posición horizontal de la estrella.
        :type x: int
        :param y: Posición vertical de la estrella.
        :type y: int
        """
        imagen = pilas.imagenes.cargar('estrella.png')
        Actor.__init__(self, imagen, x=x, y=y)
        self.rotacion = 0
