# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class Ovni(Actor):
    "Representa Ovni."

    def __init__(self, x=0, y=0):
        imagen = pilas.imagenes.cargar("ovni.png")
        Actor.__init__(self, imagen, x=x, y=y)

        self.radio_de_colision = 20
        
        self.aprender(pilas.habilidades.PuedeExplotar)

    def actualizar(self):
        pass

class Planeta(Actor):
    "Representa un planeta."

    def __init__(self, x=0, y=0, color='azul'):
        imagen = pilas.imagenes.cargar("planeta_" + color + ".png")
        Actor.__init__(self, imagen, x=x, y=y)


    def actualizar(self):
        pass
