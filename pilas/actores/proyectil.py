# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
from pilas.actores import Animacion


class Misil(Animacion):
    """Representa un misil que va en línea recta con aceleración."""

    def __init__(self, x=0, y=0, rotacion=0, velocidad_maxima=8,
                 angulo_de_movimiento=90):
        """
        Construye el Misil.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param rotacion: Angulo de rotación del Actor.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        grilla = pilas.imagenes.cargar_grilla("disparos/misil.png", 3)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.rotacion = rotacion
        self.radio_de_colision = 15

        self.hacer(pilas.comportamientos.Proyectil(velocidad_maxima=velocidad_maxima,
                                                   aceleracion=0.4,
                                                   angulo_de_movimiento=angulo_de_movimiento,
                                                   gravedad=0))

class Bala(Actor):
    """ Representa una bala que va en línea recta. """
    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=9,
                 angulo_de_movimiento=90):

        """
        Construye la Bala.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        imagen = pilas.imagenes.cargar('disparos/bola_amarilla.png')
        Actor.__init__(self, imagen)
        self.x = x
        self.y = y
        self.rotacion = rotacion

        self.radio_de_colision = 5

        self.hacer(pilas.comportamientos.Proyectil(velocidad_maxima=velocidad_maxima,
                                                   aceleracion=1,
                                                   angulo_de_movimiento=angulo_de_movimiento,
                                                   gravedad=0))

class BalaInvisible(Bala):
    """ Representa una bala que va en línea recta. """

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=9,
                 angulo_de_movimiento=90):
        super(BalaInvisible, self).__init__(x=0, y=0, rotacion=0,velocidad_maxima=9, angulo_de_movimiento=90)
        imagen = pilas.imagenes.cargar('disparos/bola_amarilla.png')

class Dinamita(Animacion):
    """ Representa un cartucho de dinamita. """

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=4,
                 angulo_de_movimiento=90):

        """
        Construye la Dinamita.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param rotacion: Angulo de rotación del Actor.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        grilla = pilas.imagenes.cargar_grilla("disparos/dinamita.png", 2)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.rotacion = rotacion
        self.radio_de_colision = 20

        self.hacer(pilas.comportamientos.Proyectil(velocidad_maxima=velocidad_maxima,
                                                   aceleracion=0.4,
                                                   angulo_de_movimiento=angulo_de_movimiento,
                                                   gravedad=3))
        self.escala = 0.7

        self.aprender(pilas.habilidades.PuedeExplotar)

    def actualizar(self):
        self.rotacion += 3


class EstrellaNinja(Actor):
    """ Representa una estrella ninja. """

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=4,
                 angulo_de_movimiento=90):

        """
        Construye la Estella Ninja.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param rotacion: Angulo de rotación del Actor.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        imagen = pilas.imagenes.cargar('disparos/estrella.png')
        Actor.__init__(self, imagen)
        self.x = x
        self.y = y
        self.rotacion = rotacion
        self.escala = 0.5
        self.radio_de_colision = 20

        self.hacer(pilas.comportamientos.Proyectil(velocidad_maxima=velocidad_maxima,
                                                   aceleracion=1,
                                                   angulo_de_movimiento=angulo_de_movimiento,
                                                   gravedad=0))

    def actualizar(self):
        self.rotacion += 10
