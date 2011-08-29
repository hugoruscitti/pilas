# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion

class Moneda(Animacion):
    """Representa una moneda con animación.
    
        >>> moneda = pilas.actores.Moneda()

    .. image:: images/actores/moneda.png
    
    """

    def __init__(self, x=0, y=0):
        Animacion.__init__(self, pilas.imagenes.cargar_grilla("moneda.png", 8), ciclica=True, x=x, y=y)
