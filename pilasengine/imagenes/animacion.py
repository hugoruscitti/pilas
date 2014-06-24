# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os

from grilla import Grilla

class Animacion(Grilla):

    def __init__(self, pilas, ruta, columnas=1, filas=1):
        Grilla.__init__(self, pilas, ruta, columnas, filas)
        self.animaciones = {}
        self.animacion_en_curso = None
        self.cuadro_en_la_animacion = 0
        self.contador_demora = 0

    def definir_animacion(self, nombre, cuadros, velocidad):
        self.animaciones[nombre] = (cuadros, velocidad)

    def cargar_animacion(self, nombre):
        self.animacion_en_curso = self.animaciones[nombre]

    def avanzar(self):
        if self.animacion_en_curso is None:
            raise Exception("Tienes que definir al menos una animacion inicial.")

        self.contador_demora += 1

        if self.contador_demora > self.animacion_en_curso[1]:
            self.cuadro_en_la_animacion += 1
            self.contador_demora = 0

            if self.cuadro_en_la_animacion >= len(self.animacion_en_curso[0]):
                self.cuadro_en_la_animacion = 0

            self.definir_cuadro(self.animacion_en_curso[0][self.cuadro_en_la_animacion])

    def __str__(self):
        nombre_imagen = os.path.basename(self.ruta_original)
        return "<Animacion del archivo '%s' (filas: %d, columnas: %d)>" % (nombre_imagen, self.filas, self.columnas)