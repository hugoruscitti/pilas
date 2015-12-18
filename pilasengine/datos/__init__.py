# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from appdirs import AppDirs


class Datos(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def generar(self, nombre):
        return DatosPersistentes(self.pilas, nombre)


class DatosPersistentes(object):

    def __init__(self, pilas, nombre):
        self.pilas = pilas
        self.dirs = AppDirs("pilasengine", nombre)
        self.datos = {}

    def guardar(self, titulo, valor):
        self.datos[titulo] = valor

    def obtener(self, titulo):
        return self.datos[titulo]
