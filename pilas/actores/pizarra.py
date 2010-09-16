# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
from PySFML import sf
import pilas

class Pizarra(Actor):
    """Representa una superficie de dibujo inicialmente transparente.

    Puedes pintar sobre esta pizarra usando métodos cómo ``dibujar_punto`` o 
    ``dibujar_cuadrado``.
    """

    def __init__(self):
        self.imagen = sf.Image(640, 480)
        self.imagen.CreateMaskFromColor(sf.Color.Black)

        Actor.__init__(self, self.imagen)

        self.punto = pilas.imagenes.cargar("punto.png")

    def dibujar_punto(self, x, y, color=sf.Color.Red):
        self.imagen.SetPixel(320 + int(x), 240 - int(y), color)
        self.pintar(self.punto, 200, 200)

    def pintar(self, imagen, x, y):
        ancho = imagen.GetWidth()
        alto = imagen.GetHeight()

        centro_x = ancho / 2
        centro_y = alto / 2

        for dx in range(ancho):
            for dy in range(alto):
                pixel = imagen.GetPixel(0 + dx, 0 + dy)

                self.imagen.SetPixel(int(320 + x + dx - centro_x), 
                                     int(240 - y + dy - centro_y), pixel)

    def dibujar_cuadrado(self, x, y, ancho=8, color=sf.Color.Black):
        # Se asegura de tener todos los valores como numeros
        # enteros.
        x = int(x)
        y = int(y)
        delta = int(ancho/2)

        inicio_x = x - delta
        fin_x = x + delta

        inicio_y = y - delta
        fin_y = y + delta

        # Recorre toda el area del cuadrado
        # dibujando uno a uno los puntos.
        for i in range(inicio_x, fin_x):
            for j in range(inicio_y, fin_y):
                self.dibujar_punto(i, j, color)
    
    def dibujar_circulo(self, x, y, color=sf.Color.Black):
        "Dibuja un circulo muy pequeño."
        self.pintar(self.punto, x, y)
