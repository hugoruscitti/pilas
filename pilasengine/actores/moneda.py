# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.animacion import Animacion


class Moneda(Animacion):
    """Representa una moneda con animación.

    .. image:: ../../pilas/data/manual/imagenes/actores/moneda.png

    Ejemplo:

        >>> moneda = pilas.actores.Moneda()

    """

    def __init__(self, pilas, x=0, y=0):
        Animacion.__init__(self, pilas, pilas.imagenes.cargar_grilla("moneda.png", 8), ciclica=True, x=x, y=y)
