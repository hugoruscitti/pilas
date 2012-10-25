# -*- encoding: utf-8 -*-
import pilas
import math

from pilas.actores.proyectil import Bala
from pilas.actores.proyectil import Misil
from pilas.actores.proyectil import Dinamita


class Municion(object):

    def __init__(self, escala=1):
        self._proyectiles = []

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        pass

    def get_proyectiles(self):
        return self._proyectiles

    def eliminar_proyectiles(self):
        self._proyectiles = []

    def agregar_proyectil(self, disparo, offset_x, offset_y):
        self.desplazar_proyectil(disparo, offset_x, offset_y)
        self._proyectiles.append(disparo)

    def desplazar_proyectil(self, disparo, offset_x, offset_y):
        rotacion_en_radianes = math.radians(-disparo.rotacion)
        dx = math.cos(rotacion_en_radianes)
        dy = math.sin(rotacion_en_radianes)

        disparo.x += dx * offset_x
        disparo.y += dy * offset_y

    proyectiles = property(get_proyectiles, None, doc="Define los disaparos de la munición.")


class DinamitaSimple(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Dinamita(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)
class BalaSimple(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)


class DobleBala(Municion):

    def __init__(self, separacion=10):
        Municion.__init__(self)
        self.separacion = separacion

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        angulo = math.radians(angulo_de_movimiento)

        self.agregar_proyectil(Bala(x=x + math.cos(angulo) * self.separacion,
                                  y=y - math.sin(angulo) * self.separacion,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

        self.agregar_proyectil(Bala(x=x - math.cos(angulo) * self.separacion,
                                  y=y + math.sin(angulo) * self.separacion,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)


class DobleBalasDesviadas(Municion):

    def __init__(self, angulo_desvio=5):
        Municion.__init__(self)
        self.angulo_desvio = angulo_desvio

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento+self.angulo_desvio,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

        self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento-self.angulo_desvio,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)


class MisilSimple(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Misil(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)
