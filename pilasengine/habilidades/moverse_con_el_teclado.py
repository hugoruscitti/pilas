# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import math

from pilasengine import habilidades


class MoverseConElTeclado(habilidades.Habilidad):
    """Hace que un actor cambie de posición con pulsar el teclado."""

    def iniciar(self, receptor, control=None, direcciones=8, velocidad_maxima=4,
                aceleracion=1, deceleracion=0.1, con_rotacion=False,
                velocidad_rotacion=1, marcha_atras=True):
        """Inicializa la habilidad.

        :param receptor: Referencia al actor que aprenderá la habilidad.
        :param control: Control al que va a responder para mover el Actor.
        :param direcciones: Establece si puede mover en cualquier direccion o
                            unicamente en 4 direcciones arriba, abajo,
                            izquierda y derecha. El parametro con_rotacion
                            establece las direcciones a 8 direcciones siempre.
        :param velocidad_maxima: Velocidad maxima en pixeles a la que se moverá
                                 el Actor.
        :param aceleracion: Indica lo rapido que acelera el actor hasta su
                            velocidad máxima.
        :param deceleracion: Indica lo rapido que decelera el actor hasta parar.
        :param con_rotacion: Si deseas que el actor rote pulsando las teclas
                             de izquierda y derecha.
        :param velocidad_rotacion: Indica lo rapido que rota un actor sobre
                                   si mismo.
        :param marcha_atras: Posibilidad de ir hacia atrás. (True o False)
        """

        super(MoverseConElTeclado, self).iniciar(receptor)

        if control is None:
            self.control = self.pilas.escena_actual().control
        else:
            self.control = control

        if not direcciones is 8 and not direcciones is 4:
            raise Exception("El parametro direcciones solo admite:\
                            el numero 4 u 8")
        else:
            self.direcciones = direcciones

        self.velocidad = 0
        self.deceleracion = deceleracion
        self._velocidad_maxima = velocidad_maxima
        self._aceleracion = aceleracion
        self.con_rotacion = con_rotacion
        self.velocidad_rotacion = velocidad_rotacion
        self.marcha_atras = marcha_atras

    def set_velocidad_maxima(self, velocidad):
        self._velocidad_maxima = velocidad

    def get_velocidad_maxima(self):
        return self._velocidad_maxima

    def get_aceleracion(self):
        return self._aceleracion

    def set_aceleracion(self, aceleracion):
        self._aceleracion = aceleracion

    velocidad_maxima = property(get_velocidad_maxima, set_velocidad_maxima,
                                doc="Define la velocidad maxima.")
    aceleracion = property(get_aceleracion, set_aceleracion,
                           doc="Define la acelaracion.")

    def actualizar(self):
        if self.con_rotacion:
            self.mover_con_rotacion()
        else:
            self.mover()

    def mover_con_rotacion(self):
        if self.control.izquierda:
            self.receptor.rotacion += (self.velocidad_rotacion *
                                       self.velocidad_maxima)
        elif self.control.derecha:
            self.receptor.rotacion -= (self.velocidad_rotacion *
                                       self.velocidad_maxima)

        if self.control.arriba:
            self.avanzar(+1)
        elif self.control.abajo:
            if self.marcha_atras:
                self.avanzar(-1)
            else:
                self.decelerar()
        else:
            self.decelerar()

        rotacion_en_radianes = math.radians(self.receptor.rotacion + 90)
        dx = math.cos(rotacion_en_radianes) * self.velocidad
        dy = math.sin(rotacion_en_radianes) * self.velocidad
        self.receptor.x += dx
        self.receptor.y += dy

    def mover(self):
        if self.direcciones == 8:
            if self.control.izquierda:
                self.receptor.x -= self.velocidad_maxima
            elif self.control.derecha:
                self.receptor.x += self.velocidad_maxima

            if self.control.arriba:
                self.receptor.y += self.velocidad_maxima
            elif self.control.abajo:
                if self.marcha_atras:
                    self.receptor.y -= self.velocidad_maxima
        else:
            if self.control.izquierda:
                self.receptor.x -= self.velocidad_maxima
            elif self.control.derecha:
                self.receptor.x += self.velocidad_maxima
            elif self.control.arriba:
                self.receptor.y += self.velocidad_maxima
            elif self.control.abajo:
                if self.marcha_atras:
                    self.receptor.y -= self.velocidad_maxima

    def decelerar(self):
        if self.velocidad > self.deceleracion:
            self.velocidad -= self.deceleracion
        elif self.velocidad < -self.deceleracion:
            self.velocidad += self.deceleracion
        else:
            self.velocidad = 0

    def avanzar(self, delta):
        self.velocidad += self.aceleracion * delta
        if self.velocidad > self.velocidad_maxima:
            self.velocidad = self.velocidad_maxima
        elif self.velocidad < - self.velocidad_maxima / 2:
            self.velocidad = - self.velocidad_maxima / 2
