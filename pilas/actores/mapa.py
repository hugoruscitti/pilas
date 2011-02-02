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

    def __init__(self, grilla, x=0, y=0, restitucion=0.56):
        Pizarra.__init__(self, x=x, y=y)
        self.grilla = grilla
        pilas.eventos.inicia_modo_depuracion.conectar(self._cuando_inicia_modo_depuracion)
        pilas.eventos.actualiza_modo_depuracion.conectar(self._cuando_actualiza_modo_depuracion)
        pilas.eventos.sale_modo_depuracion.conectar(self._cuando_sale_modo_depuracion)
        self.figuras = []
        self.restitucion = restitucion

    def pintar_bloque(self, fila, columna, indice, solido=True):
        self.grilla.definir_cuadro(indice)

        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto
        x = columna * ancho
        y = fila * alto

        self.pintar_grilla(self.grilla, x, y)

        if solido:
            dx = ancho / 2
            dy = alto / 2
            figura = pilas.fisica.Rectangulo(x - 320 + dx, 240 -y - dy, ancho, alto, dinamica=False, restitucion=self.restitucion)
            self.figuras.append(figura)

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
        self.pizarra_depuracion.deshabilitar_actualizacion_automatica()

        for columna, x in enumerate(range(0, 640, ancho)):
            for fila, y in enumerate(range(0, 480, alto)):
                self.pizarra_depuracion.dibujar_rectangulo(x, y, ancho, alto, pintar=False)
                texto = "(%d, %d)" %(fila, columna)
                self.pizarra_depuracion.escribir(texto, x=x+3, y=y+10, tamano=tamano)

        self.pizarra_depuracion.habilitar_actualizacion_automatica()

    def eliminar(self):

        # Elimina todas las figuras fisicas que ha creado.
        for x in self.figuras:
            pilas.fisica.fisica.eliminar(x)

        Pizarra.eliminar(self)
