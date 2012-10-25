# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion
import math


class Proyectil(Animacion):
    "Representa un proyectil que avanza."

    def __init__(self, grilla="sin_imagen.png", frames=1, x=0, y=0, rotacion=0,
                 velocidad_maxima=1, aceleracion=1, radio_de_colision=10,
                 angulo_de_movimiento=90):

        grilla = pilas.imagenes.cargar_grilla(grilla, frames)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)

        self.rotacion = rotacion
        self.velocidad_maxima = velocidad_maxima
        if (aceleracion == 1):
            self.velocidad = velocidad_maxima
        else:
            self.velocidad = 0
        self.aceleracion = aceleracion
        self.radio_de_colision = radio_de_colision
        self.angulo_de_movimiento = angulo_de_movimiento

    def actualizar(self):
        Animacion.actualizar(self)
        self.avanzar()

    def avanzar(self):
        """Metodo que se debe sobreescribir para implementar el comportamiento
        del Proyectil."""
        raise Exception("Debes de sobreescribir el metodo avanzar.")

    def mover_respecto_angulo_movimiento(self):
        """ Mueve el disparo hacia adelante respecto a su angulo de movimiento. """
        rotacion_en_radianes = math.radians(-self.angulo_de_movimiento + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy


class Misil(Proyectil):
    """ Representa un misil que va en línea recta con aceleración. """

    def __init__(self, x=0, y=0, rotacion=0, velocidad_maxima=8,
                 aceleracion=0.5, angulo_de_movimiento=90):

        Proyectil.__init__(self,
                         grilla="disparos/misil.png",
                         frames=3,
                         x=x,
                         y=y,
                         rotacion=rotacion,
                         velocidad_maxima=velocidad_maxima,
                         aceleracion=aceleracion,
                         radio_de_colision=15,
                         angulo_de_movimiento=angulo_de_movimiento)

    def avanzar(self):

        self.velocidad += self.aceleracion

        if self.velocidad > self.velocidad_maxima:
            self.velocidad = self.velocidad_maxima

        self.mover_respecto_angulo_movimiento()


class Bala(Proyectil):

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=9,
                 angulo_de_movimiento=90):

        Proyectil.__init__(self,
                         grilla="disparos/bola_amarilla.png",
                         frames=1,
                         x=x,
                         y=y,
                         rotacion=rotacion,
                         velocidad_maxima=velocidad_maxima,
                         aceleracion=1,
                         radio_de_colision=8,
                         angulo_de_movimiento=angulo_de_movimiento)

    def avanzar(self):
        self.mover_respecto_angulo_movimiento()


class Dinamita(Proyectil):
    """ Representa un cartucho de dinamita. """

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=4,
                 angulo_de_movimiento=90):

        Proyectil.__init__(self,
                         grilla="disparos/dinamita.png",
                         frames=2,
                         x=x,
                         y=y,
                         rotacion=rotacion,
                         velocidad_maxima=velocidad_maxima,
                         aceleracion=1,
                         radio_de_colision=20,
                         angulo_de_movimiento=angulo_de_movimiento)

        self.escala = 0.7

        self.aprender(pilas.habilidades.PuedeExplotar)

    def avanzar(self):
        self.mover_respecto_angulo_movimiento()
        self.rotacion += 3


class EstrellaNinja(Proyectil):
    """ Representa una estrella ninja. """

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=4,
                 angulo_de_movimiento=90):

        Proyectil.__init__(self,
                         grilla="disparos/estrella.png",
                         frames=1,
                         x=x,
                         y=y,
                         rotacion=rotacion,
                         velocidad_maxima=velocidad_maxima,
                         aceleracion=1,
                         radio_de_colision=20,
                         angulo_de_movimiento=angulo_de_movimiento)

        self.escala = 0.5

    def avanzar(self):
        self.mover_respecto_angulo_movimiento()
        self.rotacion += 10
