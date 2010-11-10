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

    def __init__(self, x=0, y=0):
        imagen = pilas.imagenes.cargar('tortuga.png')
        Actor.__init__(self, imagen, x=x, y=y)
        self.rotacion = 0
        self.pizarra = pilas.actores.Pizarra()
    
    def avanzar(self, pasos):
        self.hacer(pilas.comportamientos.Avanzar(self.rotacion, pasos))

    def girar(self, angulo):
        self.rotacion += angulo


    def get_y(self):
        x, y = self.GetPosition()
        return -y

    def get_x(self):
        x, y = self.GetPosition()
        return x

    def set_x(self, x):
        pilas.actores.BaseActor.set_x(self, x)

    def set_y(self, y):
        pilas.actores.BaseActor.set_y(self, y)

    x = property(get_x, set_x, doc="Define la posición horizontal.")
    y = property(get_y, set_y, doc="Define la posición vertical.")


    def ha_cambiado_posicion(self):
        self.pizarra.dibujar_circulo(self.x, self.y)
