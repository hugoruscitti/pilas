# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Pizarra

class Mapa(Pizarra):
    "Representa un escenario de bloques que tiene filas y columnas."

    def __init__(self, grilla, x=0, y=0):
        Pizarra.__init__(self, x=x, y=y)
        self.grilla = grilla

    def pintar_bloque(self, fila, columna, indice):
        self.grilla.definir_cuadro(indice)

        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto

        self.pintar_grilla(self.grilla, columna * ancho, fila * alto)
