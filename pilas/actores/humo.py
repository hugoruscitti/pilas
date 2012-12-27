# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion

class Humo(Animacion):
    """Muestra una animación de una nube de humo.

    .. image:: images/actores/humo.png

    La animación se ejecuta una vez y desaparece.

    """
    def __init__(self, x=0, y=0):
        """ Constructor del Humo

        :param x: Posición horizontal de la explosion.
        :type x: int
        :param y: Posición vertical de la explosion.
        :type y: int
        """
        grilla = pilas.imagenes.cargar_grilla("humo.png", 4)
        Animacion.__init__(self, grilla, x=x, y=y, velocidad=8)
