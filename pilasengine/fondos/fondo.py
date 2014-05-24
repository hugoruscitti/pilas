# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.actores import actor


class Fondo(actor.Actor):
    """Representa un fondo de pantalla.

    Los fondos en pilas son actores normales, solo
    que generalmente están por detrás de toda la
    escena y ocupan toda el area de la ventana.
    """
    pass