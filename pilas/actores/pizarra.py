# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
from pilas import colores
            
class Pizarra(Actor):
    """Representa una superficie de dibujo inicialmente transparente.

    Puedes pintar sobre esta pizarra usando métodos que simulan
    un lapiz, que se puede mover sobre una superficie.
    """

    def __init__(self, x=0, y=0, ancho=None, alto=None):
        # Si no define area de la pizarra toma el tamano de la ventana.
        if not ancho or not alto:
            ancho, alto = pilas.mundo.motor.obtener_area()

        Actor.__init__(self, x=x, y=y)
        self.imagen = pilas.imagenes.cargar_superficie(ancho, alto)

    def dibujar_punto(self, x, y, color=colores.negro):
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.dibujar_punto(x, y, color=color)

    def obtener_coordenada_fisica(self, x, y):
        x = (self.imagen.ancho()/2) + x
        y = (self.imagen.alto()/2) - y
        return x, y

    def pintar_imagen(self, imagen, x, y):
        self.pintar_parte_de_imagen(imagen, 0, 0, imagen.ancho(), imagen.alto(), x, y)

    def pintar_parte_de_imagen(self, imagen, origen_x, origen_y, ancho, alto, x, y):
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.pintar_parte_de_imagen(imagen, origen_x, origen_y, ancho, alto, x, y)

    def pintar_grilla(self, grilla, x, y):
        grilla.dibujarse_sobre_una_pizarra(self, x, y)

    def pintar(self, color):
        self.imagen.pintar(color)

    def linea(self, x, y, x2, y2, color=colores.negro, grosor=1):
        x, y = self.obtener_coordenada_fisica(x, y)
        x2, y2 = self.obtener_coordenada_fisica(x2, y2)
        self.imagen.linea(x, y, x2, y2, color, grosor)

    def rectangulo(self, x, y, ancho, alto, color=colores.negro, relleno=False, grosor=1):
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.rectangulo(x, y, ancho, alto, color, relleno, grosor)

    def texto(self, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro):
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.texto(cadena, x, y, magnitud, fuente, color)

    def poligono(self, puntos, color=pilas.colores.negro, grosor=1):
        puntos = [self.obtener_coordenada_fisica(*p) for p in puntos]
        self.imagen.poligono(puntos, color, grosor)
