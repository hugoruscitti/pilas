# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import math
from pilasengine import utils
from pilasengine import etiquetas

class Figura(object):
    """Representa un figura que simula un cuerpo fisico.

    Esta figura es abstracta, no está pensada para crear
    objetos a partir de ella. Se usa como base para el resto
    de las figuras cómo el Circulo o el Rectangulo simplemente."""

    def __init__(self, fisica, pilas):
        self.fisica = fisica
        self.pilas = pilas
        self.id = pilas.utils.obtener_uuid()
        self._dinamica = True
        self.figuras_en_contacto = []
        self.etiquetas = etiquetas.Etiquetas()
        self.etiquetas.agregar(self.__class__.__name__)
        self._vivo = True
        self.z = 0

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
        self._cuerpo.angle = math.radians(angulo)

    def set_x(self, x):
        self.definir_x(x)

    def get_x(self):
        return self.obtener_x()

    def set_y(self, y):
        self.definir_y(y)

    def get_y(self):
        return self.obtener_y()

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

    def get_velocidad_x(self):
        dx, _ = self.obtener_velocidad_lineal()
        return dx

    def set_velocidad_x(self, dx):
        dy = self.velocidad_y
        self.definir_velocidad_lineal(dx, dy)

    def get_velocidad_y(self):
        _, dy = self.obtener_velocidad_lineal()
        return dy

    def set_velocidad_y(self, dy):
        dx = self.velocidad_x
        self.definir_velocidad_lineal(dx, dy)

    def eliminar(self):
        """Quita una figura de la simulación."""
        if self._vivo:
            self.fisica.eliminar_figura(self._cuerpo)
            self._vivo = False

    def esta_eliminado(self):
        return not self._vivo

    def obtener_sensor(self):
        return self._sensor

    def definir_sensor(self, s):
        self._sensor = s
        #self._cuerpo.fixtures[0].sensor = s

        if s:
            self._cuerpo.gravityScale = 0
            self._cuerpo.fixtures[0].userData['sensor'] = True
        else:
            self._cuerpo.gravityScale = 1.0
            self._cuerpo.fixtures[0].userData['sensor'] = False


    def obtener_colision(self):
        return self._actor_que_representa_como_area_de_colision

    def definir_colision(self, actor):
        self._actor_que_representa_como_area_de_colision = actor
        self._cuerpo.fixtures[0].userData['actor'] = actor

    def obtener_escala_de_gravedad(self):
        return self._cuerpo.gravityScale

    def definir_escala_de_gravedad(self, s):
        self._cuerpo.gravityScale = s

    def obtener_dinamica(self):
        return self._dinamica

    def definir_dinamica(self, d):
        self._dinamica = d

        if d:
            self.escala_de_gravedad = 1
            self._cuerpo.fixtures[0].userData['dinamica'] = True
            self._cuerpo.fixedRotation = False
        else:
            self.escala_de_gravedad = 0
            self._cuerpo.fixtures[0].userData['dinamica'] = False
            self._cuerpo.fixedRotation = True

    def obtener_sin_rotacion(self):
        return self._cuerpo.fixedRotation

    def definir_sin_rotacion(self, rotacion):
        self._cuerpo.fixedRotation = rotacion

    def __repr__(self):
        return "<Figura %s en (%d, %d)>" % (self.__class__.__name__, self.x, self.y)

    x = property(get_x, set_x, doc="define la posición horizontal.")
    y = property(get_y, set_y, doc="define la posición vertical.")
    rotacion = property(get_rotation, set_rotation, doc="define la rotacion.")
    sensor = property(obtener_sensor, definir_sensor)
    actor_que_representa_como_area_de_colision = property(obtener_colision, definir_colision)
    escala_de_gravedad = property(obtener_escala_de_gravedad, definir_escala_de_gravedad)
    dinamica = property(obtener_dinamica, definir_dinamica)
    sin_rotacion = property(obtener_sin_rotacion, definir_sin_rotacion)

    velocidad_x = property(get_velocidad_x, set_velocidad_x, doc="define la velocidad horizontal.")
    velocidad_y = property(get_velocidad_y, set_velocidad_y, doc="define la velocidad vertical.")
