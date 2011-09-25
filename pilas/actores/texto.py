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

    El texto tiene atributos como ``texto``, ``magnitud`` y ``color``, por
    ejemplo para crear un mensaje de saludo podríamos escribir:

        >>> saludo = pilas.actores.Texto("Hola mundo!")


    """
    
    def __init__(self, texto="None", x=0, y=0, magnitud=20):
        imagen = pilas.mundo.motor.obtener_texto(texto, magnitud)
        self._definir_area_de_texto(texto, magnitud)
        Actor.__init__(self, imagen, x=x, y=y)
        self.magnitud = magnitud
        self.texto = texto
        self.color = pilas.colores.blanco
        self.centro = ("centro", "centro")
        self.fijo = True

    def obtener_texto(self):
        return self.imagen.texto

    def definir_texto(self, texto):
        self.imagen.texto = texto
        self._definir_area_de_texto(texto, self.magnitud)

    texto = property(obtener_texto, definir_texto, doc="El texto que se tiene que mostrar.")
    
    def obtener_magnitud(self):
        return self.imagen.magnitud
    
    def definir_magnitud(self, magnitud):
        self._magnitud = magnitud
        self.imagen.magnitud = magnitud
    
    magnitud = property(obtener_magnitud, definir_magnitud, doc="El tamaño del texto.")
    
    def obtener_color(self):
        return self.imagen.color
    
    def definir_color(self, color):
        self.imagen.color = color

    color = property(obtener_color, definir_color, doc="Color del texto.")

    def _definir_area_de_texto(self, texto, magnitud):
        self._ancho, self._alto = pilas.mundo.motor.obtener_area_de_texto(texto, magnitud)
