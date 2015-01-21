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
        self._ticks_acumulados = 0
        self.definir_animacion('inicial', [0], 1)
        self.cargar_animacion('inicial')

    def definir_animacion(self, nombre, cuadros, velocidad):
        self.animaciones[nombre] = (cuadros, velocidad)

    def cargar_animacion(self, nombre):
        if self.animacion_en_curso != self.animaciones[nombre]:
            self._ticks_acumulados = 0
            self.animacion_en_curso = self.animaciones[nombre]
            self.cuadro_en_la_animacion = 0
            self.definir_cuadro(self.animacion_en_curso[0][self.cuadro_en_la_animacion])

    def avanzar(self, velocidad=None):
        if velocidad:
            raise Exception("Tienes que definir la velocidad usando 'definir_animacion' no llamando al metodo avanzar con un numero.")

        if self.animacion_en_curso is None:
            raise Exception("Tienes que definir al menos una animacion inicial.")

        velocidad_de_animacion = (1000.0 / 60) * self.animacion_en_curso[1]
        self._ticks_acumulados += velocidad_de_animacion
        ha_avanzado = True

        if self._ticks_acumulados > 1000.0:
            self._ticks_acumulados -= 1000.0

            if self.cuadro_en_la_animacion >= len(self.animacion_en_curso[0]):
                self.cuadro_en_la_animacion = 0
                ha_avanzado = False

            self.definir_cuadro(self.animacion_en_curso[0][self.cuadro_en_la_animacion])
            self.cuadro_en_la_animacion += 1

        return ha_avanzado

    def __repr__(self):
        nombre_imagen = os.path.basename(self.ruta_original)
        return "<Animacion del archivo '%s' (filas: %d, columnas: %d)>" % (nombre_imagen, self.filas, self.columnas)
