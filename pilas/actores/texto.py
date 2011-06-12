# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from actor import Actor

class Texto(Actor):
    """Representa un texto en pantalla.

    El texto tiene atributos como ``texto``, ``magnitud`` y ``color``.
    """
    
    def __init__(self, texto="None", x=0, y=0):
        Actor.__init__(self, x=x, y=y)
        self.imagen = pilas.mundo.motor.obtener_texto(texto)
        self.texto = texto

    def obtener_texto(self):
        return self.imagen.texto

    def definir_texto(self, texto):
        self.imagen.texto = texto

    texto = property(obtener_texto, definir_texto, doc="El texto que se tiene que mostrar.")
    
    def obtener_magnitud(self):
        return self.imagen.magnitud
    
    def definir_magnitud(self, magnitud):
        self.imagen.magnitud = magnitud
    
    magnitud = property(obtener_magnitud, definir_magnitud, doc="El tamaño del texto.")
    
    def obtener_color(self):
        return self.imagen.color
    
    def definir_color(self, color):
        self.imagen.color = magnitud

    color = property(obtener_color, definir_color, doc="Color del texto.")
