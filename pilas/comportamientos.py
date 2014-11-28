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
        self.velocidad_aux = self.velocidad_inicial

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.3

        if self.receptor.y <= self.suelo:
            self.velocidad_aux /= 2.0
            self.velocidad = self.velocidad_aux

            if self.velocidad_aux <= 1:
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
        self.pasos_aux = self.pasos

    def actualizar(self):
        salir = False

        if self.pasos_aux > 0:
            if self.pasos_aux - self.velocidad < 0:
                avance = self.pasos_aux
            else:
                avance = self.velocidad
            self.pasos_aux -= avance
            self.receptor.x += self.dx * avance
            self.receptor.y += self.dy * avance
        else:
            salir = True

        if salir:
            return True

class Retroceder(Avanzar):
    "Retrocede al actor en la dirección y sentido indicado por una rotación."

    def actualizar(self):
        salir = False

        if self.pasos > 0:
            if self.pasos - self.velocidad < 0:
                avance = self.pasos
            else:
                avance = self.velocidad
            self.pasos -= avance
            self.receptor.x -= self.dx * avance
            self.receptor.y -= self.dy * avance
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


class Orbitar(Comportamiento):

    def __init__(self, x=0, y=0, radio=50, velocidad=5, direccion="derecha"):
        self.punto_de_orbita_x = x
        self.punto_de_orbita_y = y
        self.radio = radio
        self.velocidad = velocidad
        self.direccion = direccion

    def iniciar(self,receptor):
        self.receptor = receptor
        self.angulo = 0

    def actualizar(self):
        if self.direccion == "derecha":
            self.angulo += self.velocidad
            if self.angulo > 360:
                self.angulo = 1
        elif self.direccion == "izquierda":
            self.angulo -= self.velocidad
            if self.angulo < 1:
                self.angulo = 360

        self.mover_astro()

    def mover_astro(self):
        self.receptor.x = self.punto_de_orbita_x + (math.cos(math.radians(self.angulo))*self.radio)
        self.receptor.y = self.punto_de_orbita_y - (math.sin(math.radians(self.angulo))*self.radio)


class OrbitarSobreActor(Orbitar):

    def __init__(self, actor, radio=50, velocidad=5, direccion="derecha"):
        Orbitar.__init__(self, actor.x, actor.y, radio, velocidad, direccion)
        self.actor_a_orbitar = actor

    def mover_astro(self):
        self.punto_de_orbita_x = self.actor_a_orbitar.x
        self.punto_de_orbita_y = self.actor_a_orbitar.y
        Orbitar.mover_astro(self)
