# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import math
from pilasengine import utils

class Figura(object):
    """Representa un figura que simula un cuerpo fisico.

    Esta figura es abstracta, no está pensada para crear
    objetos a partir de ella. Se usa como base para el resto
    de las figuras cómo el Circulo o el Rectangulo simplemente."""

    def __init__(self, fisica, pilas):
        self.fisica = fisica
        self.pilas = pilas
        self.id = pilas.utils.obtener_uuid()
        self.actor_que_representa_como_area_de_colision = None

    def obtener_x(self):
        "Retorna la posición horizontal del cuerpo."
        return utils.convertir_a_pixels(self._cuerpo.position.x)

    def definir_x(self, x):
        """Define la posición horizontal del cuerpo.

        :param x: El valor horizontal a definir.
        """
        self._cuerpo.position = utils.convertir_a_metros(x), self._cuerpo.position.y

    def obtener_y(self):
        "Retorna la posición vertical del cuerpo."
        return utils.convertir_a_pixels(self._cuerpo.position.y)

    def definir_y(self, y):
        """Define la posición vertical del cuerpo.

        :param y: El valor vertical a definir.
        """
        self._cuerpo.position = self._cuerpo.position.x, utils.convertir_a_metros(y)

    def definir_posicion(self, x, y):
        """Define la posición para el cuerpo.

        :param x: Posición horizontal que se asignará al cuerpo.
        :param y: Posición vertical que se asignará al cuerpo.
        """
        self.definir_x(x)
        self.definir_y(y)

    def obtener_rotacion(self):
        return math.degrees(self._cuerpo.angle)

    def definir_rotacion(self, angulo):
        # TODO: simplificar a la nueva api.
        self._cuerpo.angle = math.radians(-angulo)

    #@pilas.utils.interpolable
    def set_x(self, x):
        self.definir_x(x)

    def get_x(self):
        return self.obtener_x()

    #@pilas.utils.interpolable
    def set_y(self, y):
        self.definir_y(y)

    def get_y(self):
        return self.obtener_y()

    #@pilas.utils.interpolable
    def set_rotation(self, angulo):
        self.definir_rotacion(angulo)

    def get_rotation(self):
        return self.obtener_rotacion()

    def impulsar(self, dx, dy):
        # TODO: convertir los valores dx y dy a metros.
        try:
            self._cuerpo.ApplyLinearImpulse((dx, dy), (0, 0))
        except TypeError, e:
            self._cuerpo.ApplyLinearImpulse((dx, dy), (0, 0), True)

    def obtener_velocidad_lineal(self):
        # TODO: convertir a pixels
        velocidad = self._cuerpo.linearVelocity
        return (velocidad.x, velocidad.y)

    def detener(self):
        """Hace que la figura regrese al reposo."""
        self.definir_velocidad_lineal(0, 0)

    def definir_velocidad_lineal(self, dx=None, dy=None):
        # TODO: convertir a metros
        anterior_dx, anterior_dy = self.obtener_velocidad_lineal()

        if dx is None:
            dx = anterior_dx
        if dy is None:
            dy = anterior_dy

        b2vec = self._cuerpo.linearVelocity
        b2vec.x = dx
        b2vec.y = dy

        # Añadimos el try, porque aparece el siguiente error:
        # TypeError: in method 'b2Vec2___call__', argument 2 of type 'int32'
        try:
            self._cuerpo.linearVelocity(b2vec)
        except:
            pass

    def empujar(self, dx=None, dy=None):
        # TODO: convertir a metros???
        self.definir_velocidad_lineal(dx, dy)

    def eliminar(self):
        """Quita una figura de la simulación."""
        self.fisica.eliminar_figura(self._cuerpo)

    x = property(get_x, set_x, doc="define la posición horizontal.")
    y = property(get_y, set_y, doc="define la posición vertical.")
    rotacion = property(get_rotation, set_rotation, doc="define la rotacion.")
