# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.simbolos import *

class Control:
    """Representa un control de teclado sencillo.

    Este objeto permite acceder al estado del teclado usando
    atributos.

    Por ejemplo, con este objeto, para saber si el usuario
    está pulsando el direccional hacia la izquierda de
    puede ejecutar::

        if pilas.control.izquierda:
            print 'Ha pulsado hacia la izquierda'
    """

    def __init__(self):
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.boton = False

    def actualizar(self):
        pulsa = pilas.motor.pulsa_tecla

        self.izquierda = pulsa(IZQUIERDA)
        self.derecha = pulsa(DERECHA)
        self.arriba = pulsa(ARRIBA)
        self.abajo = pulsa(ABAJO)
        self.boton = pulsa(BOTON) or pulsa(SELECCION)
