# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
import copy

class Animado(Actor):
    """Representa un actor que tiene asociada una grilla con cuadros de animacion.

    Una de las variantes que introduce este actor es el
    método 'definir_cuadro', que facilita la animación de personajes.

    Por ejemplo, si tenemos una grilla con un pingüino, podríamos
    mostrarlo usando este código:

        >>> grilla = pilas.imagenes.cargar_grilla("pingu.png", 10)
        >>> actor = Animado(grilla)
        >>> actor.definir_cuadro(2)
        >>> actor.definir_cuadro(5)


    .. image:: images/actores/pingu.png
    """

    def __init__(self, grilla, x=0, y=0):
        """ Constructor del Actor.

        :param grilla: Grilla de imagenes obtenida mediante pilas.imagenes.cargar_grilla()
        :type grilla: `Grilla`
        :param x: Posición horizontal del Actor.
        :type x: int
        :param y: Posición vertical del Actor.
        :type y: int
        """
        Actor.__init__(self, x=x, y=y)
        self.imagen = copy.copy(grilla)
        self.definir_cuadro(0)

    def definir_cuadro(self, indice):
        """ Permite cambiar el cuadro de animación a mostrar

        :param indice: Número del frame de la grilla que se quiere monstrar.
        :type indice: int
        """
        self.imagen.definir_cuadro(indice)
        # FIX: Esta sentencia es muy ambigua, porque no todos actores se deben centrar en ese punto.
        self.centro = ('centro', 'centro')
