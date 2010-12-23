# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Pizarra

class Mapa(Pizarra):
    "Representa un escenario de bloques que tiene filas y columnas."

    def __init__(self, grilla, x=0, y=0):
        Pizarra.__init__(self, x=x, y=y)
        self.grilla = grilla
        pilas.eventos.inicia_modo_depuracion.conectar(self._cuando_inicia_modo_depuracion)
        pilas.eventos.actualiza_modo_depuracion.conectar(self._cuando_actualiza_modo_depuracion)
        pilas.eventos.sale_modo_depuracion.conectar(self._cuando_sale_modo_depuracion)

    def pintar_bloque(self, fila, columna, indice):
        self.grilla.definir_cuadro(indice)

        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto

        self.pintar_grilla(self.grilla, columna * ancho, fila * alto)

    def _cuando_inicia_modo_depuracion(self, evento):
        self.pizarra_depuracion = pilas.actores.Pizarra()

        self._dibujar_rectangulos_de_la_grilla()

    def _cuando_actualiza_modo_depuracion(self, evento):
        pass
        
    def _cuando_sale_modo_depuracion(self, evento):
        self.pizarra_depuracion.eliminar()

    def _dibujar_rectangulos_de_la_grilla(self):
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto
        tamano = 8
        self.pizarra_depuracion.definir_color(pilas.colores.rojo)

        for columna, x in enumerate(range(0, 640, ancho)):
            for fila, y in enumerate(range(0, 480, alto)):
                self.pizarra_depuracion.dibujar_rectangulo(x, y, ancho, alto, pintar=False)
                texto = "(%d, %d)" %(fila, columna)
                self.pizarra_depuracion.escribir(texto, x=x+3, y=y+10, tamano=tamano)
