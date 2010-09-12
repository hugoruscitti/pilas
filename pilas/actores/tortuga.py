# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas


class Tortuga(Actor):
    "Representa una tortuga que se mueve por la pantalla como la tortuga de Logo."

    def __init__(self):
        imagen = pilas.imagenes.cargar('tortuga.png')
        Actor.__init__(self, imagen)
        self.rotacion = 0
    
    def avanzar(self, pasos):
        self.hacer(pilas.comportamientos.Avanzar(self.rotacion, pasos))

    def girar(self, angulo):
        self.rotacion += angulo
