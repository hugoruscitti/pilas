# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor



class BalasDoblesDesviadas(Actor):
    """ Representa una bala que va en línea recta. """

    @classmethod
    def instanciar(cls, pilas, x=0, y=0, rotacion=0, velocidad_maxima=9,
                 angulo_de_movimiento=90):

        b1 = pilas.actores.Bala(x=x, y=y, rotacion=rotacion, velocidad_maxima=velocidad_maxima, angulo_de_movimiento=angulo_de_movimiento - 5)
        b2 = pilas.actores.Bala(x=x, y=y, rotacion=rotacion, velocidad_maxima=velocidad_maxima, angulo_de_movimiento=angulo_de_movimiento + 5)

        return [b1, b2]
