# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import Box2D as box2d

from pilasengine.fisica.figura import Figura
from pilasengine import utils

class Rectangulo(Figura):
    """Representa un rectángulo que puede colisionar con otras figuras.

    Se puede crear un rectángulo independiente y luego asociarlo
    a un actor de la siguiente forma:

        >>> rect = pilas.fisica.Rectangulo(50, 90, True)
        >>> actor = pilas.actores.Pingu()
        >>> actor.imitar(rect)
    """

    def __init__(self, fisica, pilas, x, y, ancho, alto, dinamica=True,
                 densidad=1.0, restitucion=0.5, friccion=.2,
                 amortiguacion=0.1, sin_rotacion=False, sensor=False):

        Figura.__init__(self, fisica, pilas)

        x = utils.convertir_a_metros(x)
        y = utils.convertir_a_metros(y)
        self._ancho = utils.convertir_a_metros(ancho)
        self._alto = utils.convertir_a_metros(alto)
        self._escala = 1

        self.fisica = fisica
        self.sin_rotacion = sin_rotacion

        if not self.fisica:
            self.fisica = pilas.escena_actual().fisica

        if dinamica:
            densidad = 0

        fixture = box2d.b2FixtureDef(shape=box2d.b2PolygonShape(box=(self._ancho/2, self._alto/2)),
                                     density=densidad,
                                     linearDamping=amortiguacion,
                                     friction=friccion,
                                     restitution=restitucion)
        # Agregamos un identificador para controlarlo posteriormente en las
        # colisiones.
        self.userData = {'id': self.id, 'figura': self}
        fixture.userData = self.userData

        self._cuerpo = self.fisica.mundo.CreateDynamicBody(position=(x, y), fixtures=fixture)

        self.sensor = sensor
        self.dinamica = dinamica
        if not dinamica:
            self._cuerpo.mass = 1000000


    def definir_vertices(self):
        self._cuerpo.fixtures[0].shape.vertices = box2d.b2PolygonShape(
            box=(self._ancho/2,self._alto/2)).vertices

    def definir_escala(self, escala):
        self.ancho = (self.ancho * escala) / self.escala
        self.alto = (self.alto * escala) / self.escala
        self._escala = escala

    #@pilas.utils.interpolable
    def set_width(self, ancho):
        self._ancho = utils.convertir_a_metros(ancho)
        self.definir_vertices()

    def get_width(self):
        return utils.convertir_a_pixels(self._ancho)

    #@pilas.utils.interpolable
    def set_height(self, alto):
        self._alto = utils.convertir_a_metros(alto)
        self.definir_vertices()

    def get_height(self):
        return utils.convertir_a_pixels(self._alto)

    #@pilas.utils.interpolable
    def set_scale(self, escala):
        self.definir_escala(escala)

    def get_scale(self):
        return self._escala

    ancho = property(get_width, set_width, doc="definir ancho del rectangulo")
    alto = property(get_height, set_height, doc="definir alto del rectangulo")
    escala = property(get_scale, set_scale, doc="definir escala del rectangulo")
