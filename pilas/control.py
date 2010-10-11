# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from PySFML import sf
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
        self.izquierda = pilas.motor.pulsa_tecla(IZQUIERDA)
        self.derecha = pilas.motor.pulsa_tecla(DERECHA)
        self.arriba = pilas.motor.pulsa_tecla(ARRIBA)
        self.abajo = pilas.motor.pulsa_tecla(ABAJO)
        self.boton = pilas.motor.pulsa_tecla(BOTON)
