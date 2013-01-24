# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor

class Pausa(Actor):
    """Representa un ícono que se mostrará cuando el juego esté en pausa."""

    def __init__(self, x=0, y=0):
        """Inicia el actor de pausa.

        :param x: Posición horizontal del ícono.
        :param y: Posición vertical del ícono.
        """
        Actor.__init__(self, x=x, y=y)
        self.centro = ('centro', 'centro')
        self.imagen = "icono_pausa.png"
