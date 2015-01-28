# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import math

from pilasengine.actores.actor import Actor
from pilasengine.actores.municion import Municion
from pilasengine.actores.bala import Bala
from pilasengine import habilidades


class Disparar(habilidades.Habilidad):
    """Establece la habilidad de poder disparar un Actor o un objeto de tipo
    pilas.municion.Municion."""

    def iniciar(self, receptor, 
                 municion = Bala,
                 parametros_municion = {},
                 grupo_enemigos=[],
                 cuando_elimina_enemigo=None,
                 frecuencia_de_disparo=10,
                 angulo_salida_disparo=0,
                 offset_disparo=(0,0),
                 offset_origen_actor=(0,0),
                 cuando_dispara=None,
                 escala=1,
                 rotacion_disparo=90,
                 control=None):
        """
        Construye la habilidad.

        :param municion: Municion o Actor que se disparará.
        :param grupo_enemigos: Actores que son considerados enemigos y con los que colisionará la munición disparada.
        :param cuando_elimina_enemigo: Método que será llamado cuando se produzca un impacto con un enemigo.
        :param frecuencia_de_disparo: El número de disparos por segundo que realizará.
        :param angulo_salida_disparo: Especifica el angulo por donde saldrá el disparo efectuado por el Actor.
        :param rotacion_disparo: Rotacion del actor que representara el disparo.
        :param offset_disparo: Separación en pixeles (x,y) del disparo con respecto al centro del Actor.
        :param offset_origen_actor: Si el Actor no tiene su origen en el centro, con este parametro podremos colocar correctamente el disparo.
        :param cuando_dispara: Metodo que será llamado cuando se produzca un disparo.
        :param escala: Escala de los actores que serán disparados.
        :param control: Indica los controles que utiliza el actor para saber cuando pulsa el botón de disparar.

        :example:

        >>> mono = pilas.actores.Mono()
        >>> mono.aprender(pilas.habilidades.Disparar,
        >>>               municion=pilas.actores.proyectil.Bala,
        >>>               grupo_enemigos=enemigos,
        >>>               cuando_elimina_enemigo=eliminar_enemigo)

        ..
        """

        super(Disparar, self).iniciar(receptor)

        self._municion = municion
        self.parametros_municion = parametros_municion

        self.offset_disparo_x = offset_disparo[0]
        self.offset_disparo_y = offset_disparo[1]

        self.offset_origen_actor_x = offset_origen_actor[0]
        self.offset_origen_actor_y = offset_origen_actor[1]

        self.angulo_salida_disparo = angulo_salida_disparo
        self.rotacion_disparo = rotacion_disparo
        self.frecuencia_de_disparo = frecuencia_de_disparo
        self.contador_frecuencia_disparo = 0
        self.proyectiles = []
        
        print(self.angulo_salida_disparo)

        self.grupo_enemigos = grupo_enemigos

        self.definir_colision(self.grupo_enemigos, cuando_elimina_enemigo)

        self.cuando_dispara = cuando_dispara

        self.escala = escala

        self.control = control

    def set_frecuencia_de_disparo(self, valor):
        self._frecuencia_de_disparo = 60 / valor

    def get_frecuencia_de_disparo(self):
        return self._frecuencia_de_disparo

    def set_municion(self, valor):
        self._municion = valor
        self.parametros_municion = {}

    def get_municion(self):
        return self._municion

    frecuencia_de_disparo = property(get_frecuencia_de_disparo, set_frecuencia_de_disparo, doc="Número de disparos por segundo.")
    municion = property(get_municion, set_municion, doc="Establece el tipo de municion que dispara.")

    def definir_colision(self, grupo_enemigos, cuando_elimina_enemigo):
        self.grupo_enemigos = grupo_enemigos
        self.pilas.colisiones.agregar(self.proyectiles, self.grupo_enemigos,
                                                 cuando_elimina_enemigo)
    def actualizar(self):
        self.contador_frecuencia_disparo += 1

        if self.pulsa_disparar():
            if self.contador_frecuencia_disparo > self._frecuencia_de_disparo:
                self.contador_frecuencia_disparo = 0
                self.disparar()

        #self._eliminar_disparos_innecesarios()

    def _agregar_disparo(self, proyectil):
        proyectil.escala = self.escala
        self._desplazar_proyectil(proyectil, self.offset_disparo_x, self.offset_disparo_y)
        self.proyectiles.append(proyectil)

    def _desplazar_proyectil(self, proyectil, offset_x, offset_y):
        rotacion_en_radianes = math.radians(-proyectil.rotacion)
        dx = math.cos(rotacion_en_radianes)
        dy = math.sin(rotacion_en_radianes)

        proyectil.x += dx * offset_x
        proyectil.y += dy * offset_y

    def disparar(self):
        if (self.receptor.espejado):
            offset_origen_actor_x = -self.offset_origen_actor_x
        else:
            offset_origen_actor_x = self.offset_origen_actor_x

        if issubclass(self.municion, Municion):

            objeto_a_disparar = self.municion(**self.parametros_municion)

            objeto_a_disparar.disparar(x=self.receptor.x+offset_origen_actor_x,
                                   y=self.receptor.y+self.offset_origen_actor_y,
                                   angulo_de_movimiento=self.receptor.rotacion + (self.angulo_salida_disparo),
                                   rotacion=self.receptor.rotacion + -(self.rotacion_disparo),
                                   offset_disparo_x=self.offset_disparo_x,
                                   offset_disparo_y=self.offset_disparo_y)

            for disparo in objeto_a_disparar.proyectiles:
                self._agregar_disparo(disparo)
                disparo.fijo = self.receptor.fijo

        elif issubclass(self.municion, Actor):

            objeto_a_disparar = self.municion(pilas=self.pilas, x=self.receptor.x+offset_origen_actor_x,
                                              y=self.receptor.y+self.offset_origen_actor_y,
                                              rotacion=self.receptor.rotacion + -(self.rotacion_disparo),
                                              angulo_de_movimiento=self.receptor.rotacion + (self.angulo_salida_disparo))

            self._agregar_disparo(objeto_a_disparar)
            objeto_a_disparar.fijo = self.receptor.fijo
        else:
            raise "No se puede disparar este objeto."

        if self.cuando_dispara:
            self.cuando_dispara()


    def eliminar(self):
        pass

    def pulsa_disparar(self):
        return self.control.boton if self.control else self.pilas.control.boton                
