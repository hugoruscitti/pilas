# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class Menu(Actor):
    "Representa un bloque que tiene fisica como una caja."

    def __init__(self, opciones, x=0, y=0):
        Actor.__init__(self, "invisible.png", x=x, y=y)
        self._verificar_opciones(opciones)
        self.crear_texto_de_las_opciones(opciones)
        self.opciones = opciones
        self.seleccionar_primer_opcion()
        self.opcion_actual = 0

    def crear_texto_de_las_opciones(self, opciones):
        "Genera un actor por cada opcion del menu."
        self.opciones_como_actores = []

        for indice, (texto, funcion) in enumerate(opciones):
            y = self.y - indice * 50
            opciones = pilas.actores.Opcion(texto, y=y, funcion_a_invocar=funcion)
            self.opciones_como_actores.append(opciones)

    def seleccionar_primer_opcion(self):
        if self.opciones_como_actores:
            self.opciones_como_actores[0].resaltar()

    def _verificar_opciones(self, opciones):
        "Se asegura de que la lista este bien definida."

        for x in opciones:
            if not isinstance(x, tuple) or len(x) != 2:
                raise Exception("Opciones incorrectas, cada opcion tiene que ser una tupla.")

    def actualizar(self):
        "Se ejecuta de manera periodica."
        if pilas.mundo.control.boton:
            self.seleccionar_opcion_actual()

    def seleccionar_opcion_actual(self):
        opcion = self.opciones_como_actores[self.opcion_actual]
        opcion.seleccionar()
