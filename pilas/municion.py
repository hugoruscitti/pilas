# -*- encoding: utf-8 -*-
import math

from pilas.actores.proyectil import Bala
from pilas.actores.proyectil import Misil


class Municion(object):
    """ Clase base para representar un conjunto de proyectiles que pueden
    ser disparados mediante la habilidad de Disparar.
    """

    def __init__(self):
        self._proyectiles = []

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        """ Este método debe ser sobreescrito.
        En él se deben crear los proyectiles y agregarlos a la lista de proyectiles

        >>>         self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

        """
        raise Exception("No ha sobreescrito el metodo disparar.")

    def agregar_proyectil(self, proyectil):
        """ Agrega un proyectil a la lista de proyectiles de la munición. """
        self._proyectiles.append(proyectil)

    def get_proyectiles(self):
        """ Obtiene los proyectiles que acaba de disparar la munición. """
        return self._proyectiles

    proyectiles = property(get_proyectiles, None, doc="Define los disaparos de la munición.")

class BalaDoble(Municion):
    """ Munición que dispara 2 balas paralelas. """

    def __init__(self, separacion=10):
        Municion.__init__(self)
        self.separacion = separacion

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        angulo = math.radians(angulo_de_movimiento)

        self.agregar_proyectil(Bala(x=x + math.cos(angulo) * self.separacion,
                                    y=y - math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion))

        self.agregar_proyectil(Bala(x=x - math.cos(angulo) * self.separacion,
                                    y=y + math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion))


class BalasDoblesDesviadas(Municion):
    """ Munición que dispara 2 balas en angulos distintos. """

    def __init__(self, angulo_desvio=5):
        Municion.__init__(self)
        self.angulo_desvio = angulo_desvio

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento+self.angulo_desvio,
                                  rotacion=rotacion))

        self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento-self.angulo_desvio,
                                  rotacion=rotacion))

class MisilDoble(Municion):
    """ Munición que dispara 2 misiles paralelos que aceleran poco a poco. """

    def __init__(self, separacion=10):
        Municion.__init__(self)
        self.separacion = separacion

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        angulo = math.radians(angulo_de_movimiento)

        self.agregar_proyectil(Misil(x=x + math.cos(angulo) * self.separacion,
                                    y=y - math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion))

        self.agregar_proyectil(Misil(x=x - math.cos(angulo) * self.separacion,
                                    y=y + math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion))
