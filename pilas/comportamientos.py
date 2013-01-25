# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import math
import pilas

class Comportamiento(object):
    "Representa un comportamiento (estrategia) que se puede anexar a un actor."

    def iniciar(self, receptor):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        self.receptor = receptor

    def actualizar(self):
        """Actualiza el comportamiento en un instante dado.

        Si este metodo retorna True entonces el actor dejará
        de ejecutar este comportamiento."""
        pass

    def terminar(self):
        pass


class Girar(Comportamiento):
    "Hace girar constantemente al actor respecto de su eje de forma relativa."

    def __init__(self, delta, velocidad):
        self.delta = delta

        if delta > 0:
            self.velocidad = velocidad
        else:
            self.velocidad = -velocidad

    def iniciar(self, receptor):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        self.receptor = receptor
        self.angulo_final = (receptor.rotacion + self.delta) % 360

    def actualizar(self):
        self.receptor.rotacion += self.velocidad

        delta = abs(self.receptor.rotacion - self.angulo_final)

        if delta <= abs(self.velocidad):
            self.receptor.rotacion = self.angulo_final
            return True

class Saltar(Comportamiento):
    """Realiza un salto, cambiando los atributos 'y'."""

    def __init__(self, velocidad_inicial=10, cuando_termina=None):
        self.velocidad_inicial = velocidad_inicial
        self.cuando_termina = cuando_termina
        self.sonido_saltar = pilas.sonidos.cargar("saltar.wav")

    def iniciar(self, receptor):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        self.receptor = receptor
        self.suelo = int(self.receptor.y)
        self.velocidad = self.velocidad_inicial
        self.sonido_saltar.reproducir()

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.3

        if self.receptor.y <= self.suelo:
            self.velocidad_inicial /= 2.0
            self.velocidad = self.velocidad_inicial

            if self.velocidad_inicial <= 1:
                # Si toca el suelo
                self.receptor.y = self.suelo
                if self.cuando_termina:
                    self.cuando_termina()
                return True


class Avanzar(Comportamiento):
    "Desplaza al actor en la dirección y sentido indicado por una rotación."

    def __init__(self, pasos=0, velocidad=5):
        if pasos < 0:
            self.pasos = abs(pasos)
        else:
            self.pasos = pasos

        self.velocidad = velocidad

    def iniciar(self, receptor):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        self.receptor = receptor
        rotacion_en_radianes = math.radians(-receptor.rotacion)
        self.dx = math.cos(rotacion_en_radianes)
        self.dy = math.sin(rotacion_en_radianes)

    def actualizar(self):
        salir = False

        if self.pasos > 0:
            if self.pasos - self.velocidad < 0:
                avance = self.pasos
            else:
                avance = self.velocidad
            self.pasos -= avance
            self.receptor.x += self.dx * avance
            self.receptor.y += self.dy * avance
        else:
            salir = True

        if salir:
            return True

class Proyectil(Comportamiento):
    "Hace que un actor se comporte como un proyectil."

    def __init__(self, velocidad_maxima=5, aceleracion=1,
                 angulo_de_movimiento=90, gravedad=0):
        """
        Construye el comportamiento.

        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param aceleracion: Valor entre 0 y 1 para indicar lo rápido que acelerará el actor.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor.
        :param gravedad: La velocidad vertical con la que caerá el actor.

        """
        self._velocidad_maxima = velocidad_maxima
        self._aceleracion = aceleracion
        self._angulo_de_movimiento = angulo_de_movimiento
        self._gravedad = gravedad
        self._vy = self._gravedad

        if (self._aceleracion == 1):
            self._velocidad = self._velocidad_maxima
        else:
            self._velocidad = 0

    def iniciar(self, receptor):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        self.receptor = receptor

    def actualizar(self):
        self._velocidad += self._aceleracion

        if self._velocidad > self._velocidad_maxima:
            self._velocidad = self._velocidad_maxima

        self.mover_respecto_angulo_movimiento()

    def mover_respecto_angulo_movimiento(self):
        """Mueve el actor hacia adelante respecto a su angulo de movimiento."""
        rotacion_en_radianes = math.radians(-self._angulo_de_movimiento + 90)
        dx = math.cos(rotacion_en_radianes) * self._velocidad
        dy = math.sin(rotacion_en_radianes) * self._velocidad
        self.receptor.x += dx

        if self._gravedad > 0:
            self.receptor.y += dy + self._vy
            self._vy -= 0.1
        else:
            self.receptor.y += dy
