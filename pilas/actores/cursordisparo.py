# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class CursorDisparo(Actor):
    "Representa un bloque que tiene fisica como una caja."

    def __init__(self, x=0, y=0):
        imagen = pilas.imagenes.cargar('cursordisparo.png')
        Actor.__init__(self, imagen)
        self.rotacion = 0
        self.x = x
        self.y = y
        self.radio_de_colision = 25

        self.aprender(pilas.habilidades.SeguirAlMouse)
        pilas.mundo.motor.ocultar_puntero_del_mouse()
