# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
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
        """ Este método debe ser sobreescrito."""
        raise Exception("No ha sobreescrito el metodo disparar.")

    def agregar_proyectil(self, proyectil):
        """ Agrega un proyectil a la lista de proyectiles de la munición.

        :param proyectil: Actor que se añadirá a la lista de proyectiles."""
        self._proyectiles.append(proyectil)

    def get_proyectiles(self):
        """ Obtiene los proyectiles que acaba de disparar la munición. """
        return self._proyectiles

    proyectiles = property(get_proyectiles, None, doc="Obtiene los proyectiles de la munición.")


class BalaDoble(Municion):
    """ Munición que dispara 2 balas paralelas. """

    def __init__(self, separacion=10):
        """
        Construye la Munición.

        :param separacion: Separación en pixeles entre los dos proyectiles.
        """

        Municion.__init__(self)
        self.separacion = separacion

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        """Realiza un disparo.

        :param x: Posición horizontal desde donde comenzará a disparar.
        :param y: Posición vertical desde donde comenzará a disparar.
        :param angulo_de_movimiento: Angulo de inclinación inicial del disparo.
        :param offset_disparo_x: Desplazamiento del disparo horizontal.
        :param offset_disparo_y: Desplazamiento del disparo vertical.
        """
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
        """
        Construye la Munición.

        :param angulo_desvio: Angulo que formarán los dos proyectiles.
        """

        Municion.__init__(self)
        self.angulo_desvio = angulo_desvio

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        """Realiza un disparo.

        :param x: Posición horizontal desde donde comenzará a disparar.
        :param y: Posición vertical desde donde comenzará a disparar.
        :param angulo_de_movimiento: Angulo de inclinación inicial del disparo.
        :param offset_disparo_x: Desplazamiento del disparo horizontal.
        :param offset_disparo_y: Desplazamiento del disparo vertical.
        """

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
        """
        Construye la Munición.

        :param separacion: Separación en pixeles entre los dos proyectiles.
        """
        Municion.__init__(self)
        self.separacion = separacion

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        """Realiza un disparo.

        :param x: Posición horizontal desde donde comenzará a disparar.
        :param y: Posición vertical desde donde comenzará a disparar.
        :param angulo_de_movimiento: Angulo de inclinación inicial del disparo.
        :param offset_disparo_x: Desplazamiento del disparo horizontal.
        :param offset_disparo_y: Desplazamiento del disparo vertical.
        """

        angulo = math.radians(angulo_de_movimiento)

        self.agregar_proyectil(Misil(x=x + math.cos(angulo) * self.separacion,
                                    y=y - math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion))

        self.agregar_proyectil(Misil(x=x - math.cos(angulo) * self.separacion,
                                    y=y + math.sin(angulo) * self.separacion,
                                    angulo_de_movimiento=angulo_de_movimiento,
                                    rotacion=rotacion))
