# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Controlador(Actor):

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar('invisible.png')
        self.radio_de_colision = None
        self.dy = self.y
        self.distancia = 25
        self.manejadores = []

    def agregar(self, actor, propiedad, minimo, maximo):
        x = self.x
        y = self.y - self.dy

        mp = self.pilas.actores.ManejadorPropiedad(x, y, actor,
                                                   propiedad,
                                                   minimo, maximo)
        self.dy += self.distancia
        self.manejadores.append(mp)

    def agregar_espacio(self):
        self.y -= 10