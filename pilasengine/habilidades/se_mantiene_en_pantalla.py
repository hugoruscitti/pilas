# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades


class SeMantieneEnPantalla(habilidades.Habilidad):
    """Se asegura de que el actor regrese a la pantalla si sale o que no
    salga en nigún momento de la pantalla.

    Si el actor sale por la derecha de la pantalla, entonces regresa
    por la izquiera. Si sale por arriba regresa por abajo y asi...

    """
    def iniciar(self, receptor, permitir_salida=True):
        """
        :param receptor: El actor que aprenderá la habilidad.
        :param permitir_salida: Valor booleano que establece si el actor
                                puede salir por los lados de la ventana y
                                regresar por el lado opuesto. Si se establece a
                                False, el actor no puede salir de la ventana en
                                ningún momento.
        """
        super(SeMantieneEnPantalla, self).iniciar(receptor)
        self.ancho, self.alto = self.pilas.obtener_area()
        self.permitir_salida = permitir_salida

    def actualizar(self):
        if self.permitir_salida:
            # Se asegura de regresar por izquierda y derecha.
            if self.receptor.derecha < -(self.ancho/2):
                self.receptor.izquierda = (self.ancho/2)
            elif self.receptor.izquierda > (self.ancho/2):
                self.receptor.derecha = -(self.ancho/2)

            # Se asegura de regresar por arriba y abajo.
            if self.receptor.abajo > (self.alto/2):
                self.receptor.arriba = -(self.alto/2)
            elif self.receptor.arriba < -(self.alto/2):
                self.receptor.abajo = (self.alto/2)
        else:
            if self.receptor.izquierda <= -(self.ancho/2):
                self.receptor.izquierda = -(self.ancho/2)
            elif self.receptor.derecha >= (self.ancho/2):
                self.receptor.derecha = self.ancho/2

            if self.receptor.arriba > (self.alto/2):
                self.receptor.arriba = (self.alto/2)
            elif self.receptor.abajo < -(self.alto/2):
                self.receptor.abajo = -(self.alto/2)