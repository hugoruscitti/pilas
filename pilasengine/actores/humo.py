# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.animacion import Animacion


class Humo(Animacion):
    """Muestra una animación de una nube de humo.

    .. image:: ../../pilas/data/manual/imagenes/actores/humo.png

    La animación se ejecuta una vez y desaparece.

    """
    def __init__(self, pilas, x, y):
        grilla = pilas.imagenes.cargar_grilla("humo.png", 4)
        Animacion.__init__(self, pilas, grilla, ciclica=False, x=x, y=y,
                           velocidad=8)
