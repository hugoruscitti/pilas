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

class Disparo(Animacion):
    "Representa un disparo que avanza."

    def __init__(self, grilla="sin_imagen.png", frames=1, x=0, y=0, rotacion=0,
                 velocidad_maxima=1, aceleracion=1, radio_de_colision=10,
                 angulo_de_movimiento=90):
        grilla = pilas.imagenes.cargar_grilla(grilla, frames)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = radio_de_colision
        self.rotacion = rotacion
        self.velocidad_maxima = velocidad_maxima
        self.velocidad = 0
        self.aceleracion = aceleracion
        self.radio_de_colision = radio_de_colision
        self.angulo_de_movimiento = angulo_de_movimiento

    def actualizar(self):
        Animacion.actualizar(self)
        self.avanzar()

    def avanzar(self):
        "Hace avanzar la nave en direccion a su angulo."
        rotacion_en_radianes = math.radians(-self.rotacion + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy

class Misil(Disparo):

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=8,aceleracion=0.5,
                 angulo_de_movimiento=90):

        Disparo.__init__(self,
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

        rotacion_en_radianes = math.radians(-self.angulo_de_movimiento + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy

class MisilGuiado(Disparo):

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=8,aceleracion=0.5,
                 angulo_de_movimiento=90):

        Disparo.__init__(self,
                         grilla="disparos/misil.png",
                         frames=3,
                         x=x,
                         y=y,
                         rotacion=rotacion,
                         velocidad_maxima=velocidad_maxima,
                         aceleracion=aceleracion,
                         radio_de_colision=15,
                         angulo_de_movimiento=angulo_de_movimiento)

        self.actor_mas_cercano = pilas.utils.actor_mas_cercano_al_actor(self)

        if (self.actor_mas_cercano):
            self.aprender(pilas.habilidades.MirarAlActor, self.actor_mas_cercano)

    def avanzar(self):
        if not(self.actor_mas_cercano._vi):
            self.eliminar()

        self.velocidad += self.aceleracion

        if self.velocidad > self.velocidad_maxima:
            self.velocidad = self.velocidad_maxima

        rotacion_en_radianes = math.radians(-self.rotacion + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.x += dx
        self.y += dy


class Bala(Disparo):

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=9,
                 angulo_de_movimiento=90):

        Disparo.__init__(self,
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
        rotacion_en_radianes = math.radians(-self.angulo_de_movimiento + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad_maxima
        dy = math.sin(rotacion_en_radianes) * self.velocidad_maxima
        self.x += dx
        self.y += dy

class Dinamita(Disparo):

    def __init__(self,x=0,y=0,rotacion=0,velocidad_maxima=4,
                 angulo_de_movimiento=90):

        Disparo.__init__(self,
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
        rotacion_en_radianes = math.radians(-self.angulo_de_movimiento + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad_maxima
        dy = math.sin(rotacion_en_radianes) * self.velocidad_maxima
        self.x += dx
        self.y += dy
        self.rotacion += 3

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

    def __init__(self):
        Municion.__init__(self)

    def disparar(self, x, y, rotacion, angulo_de_movimiento, offset_disparo_x, offset_disparo_y):
        angulo = math.radians(angulo_de_movimiento)

        self.agregar_disparo(Bala(x=x + math.cos(angulo) * 10,
                                  y=y - math.sin(angulo) * 10,
                                  angulo_de_movimiento=angulo_de_movimiento,
                                  rotacion=rotacion),
                             offset_disparo_x,
                             offset_disparo_y)

        self.agregar_disparo(Bala(x=x - math.cos(angulo) * 10,
                                  y=y + math.sin(angulo) * 10,
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

