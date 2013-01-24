# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class Pelota(Actor):
    """Representa una pelota de Volley, que puede rebotar e interactuar con la física del escenario."""

    def __init__(self, x=0, y=0):
        """Construye una pelota y define la posición inicial.

        :param x: Posición horizontal inicial.
        :param y: posición vertical inicial.
        """
        imagen = pilas.imagenes.cargar('pelota.png')
        Actor.__init__(self, imagen)
        self.rotacion = 0
        self.x = x
        self.y = y
        self.radio_de_colision = 25

        self.aprender(pilas.habilidades.RebotarComoPelota)
