# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.fisica.figura import Figura

class Poligono(Figura):
    """Representa un cuerpo poligonal.

    El poligono necesita al menos tres puntos para dibujarse, y cada
    uno de los puntos se tienen que ir dando en orden de las agujas
    del reloj.

    Por ejemplo:

        >>> pilas.fisica.Poligono(0,0,[(100, 2), (-50, 0), (-100, 100.0)])

    """

    def __init__(self, x, y, puntos, dinamica=True, densidad=1.0,
            restitucion=0.56, friccion=10.5, amortiguacion=0.1,
            fisica=None, sin_rotacion=False, sensor=False):

        Figura.__init__(self)

        self._escala = 1

        self.puntos = puntos
        self.dinamica = dinamica
        self.fisica = fisica

        if not self.fisica:
            self.fisica = pilas.escena_actual().fisica

        self.vertices = [(convertir_a_metros(x1) * self._escala, convertir_a_metros(y1) * self._escala) for (x1, y1) in self.puntos]

        fixture = box2d.b2FixtureDef(shape=box2d.b2PolygonShape(vertices=self.vertices),
                                     density=densidad,
                                     linearDamping=amortiguacion,
                                     friction=friccion,
                                     restitution=restitucion)

        self.userData = {'id': self.id, 'figura': self}
        fixture.userData = self.userData

        if self.dinamica:
            self._cuerpo = self.fisica.mundo.CreateDynamicBody(position=(0, 0), fixtures=fixture)
        else:
            self._cuerpo = self.fisica.mundo.CreateKinematicBody(position=(0, 0), fixtures=fixture)

        self.sin_rotacion = sin_rotacion
        self.sensor = sensor


    def definir_escala(self, escala):
        self._escala = escala
        self.vertices = [(convertir_a_metros(x1) * self._escala, convertir_a_metros(y1) * self._escala) for (x1, y1) in self.puntos]
        self._cuerpo.fixtures[0].shape.vertices = box2d.b2PolygonShape(
            vertices = self.vertices).vertices


    @pilas.utils.interpolable
    def set_scale(self, escala):
        self.definir_escala(escala)


    def get_scale(self):
        return self._escala

    escala = property(get_scale, set_scale, doc="definir escala del poligono")
