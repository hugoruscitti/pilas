# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas
import pymunk

def add_ball(space, x, y):
    mass = 1
    radius = 25
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = x, y
    body.elasticity = 0.95
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape


class Pelota(Actor):
    "Representa una pelota de Volley."

    def __init__(self, x=0, y=0):
        imagen = pilas.imagenes.cargar('pelota.png')
        Actor.__init__(self, imagen)
        self.rotacion = 0
        self.x = x
        self.y = y
        self.figura = self._crear_figura()

    def actualizar(self):
        self.x = self.figura.body.position.x
        self.y = self.figura.body.position.y
        self.rotacion = self.figura.body.angle * 1000000000000000000

    def _crear_figura(self):
        return add_ball(pilas.fisica.fisica.espacio, self.x, self.y)
