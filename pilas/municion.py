# -*- encoding: utf-8 -*-
import pilas
import math

from pilas.actores.proyectil import Bala
from pilas.actores.proyectil import Misil
from pilas.actores.proyectil import Dinamita
from pilas.actores.proyectil import EstrellaNinja


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

    def agregar_proyectil(self, disparo):
        """ Agrega un proyectil a la lista de proyectiles de la munición. """
        self._proyectiles.append(disparo)

    def get_proyectiles(self):
        """ Obtiene los proyectiles que acaba de disparar la munición. """
        return self._proyectiles

    proyectiles = property(get_proyectiles, None, doc="Define los disaparos de la munición.")


class DinamitaSimple(Municion):
    """ Munición que dispara un cartucho de dinamita. """

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Dinamita(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

class EstrellaNinjaSimple(Municion):
    """ Munición que dispara una estrella ninja. """

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(EstrellaNinja(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

class BalaSimple(Municion):
    """ Munición que dispara una bala. """

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Bala(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)


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
    """ Munición que dispara 1 misil que acelera poco a poco. """

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):

        self.agregar_proyectil(Misil(x=x,
                                  y=y,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

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
                                    rotacion=rotacion),
                               offset_disparo_x,
                               offset_disparo_y)

        self.agregar_proyectil(Misil(x=x - math.cos(angulo) * self.separacion,
                                    y=y + math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion),
                               offset_disparo_x,
                               offset_disparo_y)
