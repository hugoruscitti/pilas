# -*- encoding: utf-8 -*-
import pilas
import math

from pilas.actores.proyectil import Bala
from pilas.actores.proyectil import Misil
from pilas.actores.proyectil import Dinamita


class Municion(object):

    def __init__(self):
        self._disparos = []

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        pass

    def get_disparos(self):
        return self._disparos

    def eliminar_disparos(self):
        self._disparos = []

    def agregar_disparo(self, disparo, offset_x, offset_y):
        self.desplazar_disparo(disparo, offset_x, offset_y)
        self._disparos.append(disparo)

    def desplazar_disparo(self, disparo, offset_x, offset_y):
        rotacion_en_radianes = math.radians(-disparo.rotacion)
        dx = math.cos(rotacion_en_radianes)
        dy = math.sin(rotacion_en_radianes)

        disparo.x += dx * offset_x
        disparo.y += dy * offset_y

    disparos = property(get_disparos, None, doc="Define los disaparos de la munición.")


class DinamitaSimple(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_disparo(Dinamita(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)
class BalaSimple(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_disparo(Bala(x=x,
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

        self.agregar_disparo(Bala(x=x + math.cos(angulo) * self.separacion,
                                  y=y - math.sin(angulo) * self.separacion,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

        self.agregar_disparo(Bala(x=x - math.cos(angulo) * self.separacion,
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

        self.agregar_disparo(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento+self.angulo_desvio,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

        self.agregar_disparo(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento-self.angulo_desvio,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

class MisilSimple(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_disparo(Misil(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

class MisilGuiadoAlActor(Municion):

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_disparo(MisilGuiado(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

