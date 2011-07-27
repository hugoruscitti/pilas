# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Texto

class Opcion(Texto):

    def __init__(self, texto, x=0, y=0, funcion_a_invocar=None):
        Texto.__init__(self, texto, x=x, y=y)
        self.magnitud = 20
        self.funcion_a_invocar = funcion_a_invocar
        self.color = pilas.colores.gris
        self.z = -300
        self.centro = ("centro", "centro")

    def resaltar(self, estado=True):
        "Pinta la opcion actual de un color mas claro."

        if estado:
            self.color = pilas.colores.blanco
        else:
            self.color = pilas.colores.gris

    def seleccionar(self):
        "Invoca a la funcion que tiene asociada para ejecutar."

        if self.funcion_a_invocar:
            self.funcion_a_invocar()
        else:
            print "Cuidado, la opcion", self, "no tiene funcion asociada."
