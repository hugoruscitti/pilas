# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from PySFML import sf

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


    def __init__(self, input):
        self.input = input

        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.boton = False

    def actualizar(self):
        self.izquierda = self.input.IsKeyDown(sf.Key.Left) 
        self.derecha = self.input.IsKeyDown(sf.Key.Right) 
        self.arriba = self.input.IsKeyDown(sf.Key.Up) 
        self.abajo = self.input.IsKeyDown(sf.Key.Down) 
        self.boton = self.input.IsKeyDown(sf.Key.Space) or self.input.IsKeyDown(sf.Key.Return)
