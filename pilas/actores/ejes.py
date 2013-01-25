# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor

class Ejes(Actor):
    """Representa el eje de coordenadas tomado como sistema de referencia.

    Este actor es útil para mostrar que la ventana
    de pilas tiene una referencia, y que las posiciones
    responden a este modelo.

    Para crear el eje podrías ejecutar:

        >>> eje = pilas.actore.Eje()

    """

    def __init__(self, x=0, y=0):
        """ Constructor de los ejes.

        :param x: Posición horizontal de los ejes.
        :type x: int
        :param y: Posición vertical de los ejes.
        :type y: int
        """
        Actor.__init__(self, "ejes.png", x=x, y=y)
        self.z = 100
