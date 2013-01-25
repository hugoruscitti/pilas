# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class Ovni(Actor):
    """Representa Ovni que explota al momento de ser eliminado.

        .. image:: images/actores/ovni.png

    """

    def __init__(self, x=0, y=0):
        """Constructor de la Ovni

        :param x: Posición horizontal del ovni.
        :type x: int
        :param y: Posición vertical del ovni.
        :type y: int

        """
        imagen = pilas.imagenes.cargar("ovni.png")
        Actor.__init__(self, imagen, x=x, y=y)

        self.radio_de_colision = 20

        self.aprender(pilas.habilidades.PuedeExplotar)

    def actualizar(self):
        pass


class Planeta(Actor):
    """Representa un planeta para utilizar con el ovni.

        .. image:: images/actores/planeta_azul.png

    """

    def __init__(self, x=0, y=0, color='azul'):
        """Constructor del planeta.

        :param x: Posición horizontal del planeta.
        :type x: int
        :param y: Posición vertical del planeta.
        :type y: int
        :param color: El color del planeta
        :type color: Puede ser ``azul``, ``marron``, ``naranja``, ``rojo`` o ``verde``
        """

        imagen = pilas.imagenes.cargar("planeta_{}.png".format(color))
        Actor.__init__(self, imagen, x=x, y=y)


    def actualizar(self):
        pass
