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
        """Inicializa el actor Pizarra.

        :param x: Posición horizontal inicial.
        :param y: Posición horizontal inicial.
        :param ancho: El tamaño horizontal en pixels, si no se especifica será el tamaño de la ventana.
        :param alto: El tamaño vertical en pixels, si no se especifica será el tamaño de la ventana.
        """
        # Si no define area de la pizarra toma el tamano de la ventana.
        if not ancho or not alto:
            ancho, alto = pilas.mundo.obtener_area()

        Actor.__init__(self, x=x, y=y)
        self.imagen = pilas.imagenes.cargar_superficie(ancho, alto)

    def dibujar_punto(self, x, y, color=colores.negro):
        """Dibuja un punto sobre la pizarra.

        El punto será 3 pixels de radio, y si no se especifica tendrá
        color negro.

        Este es un ejemplo de invocación:

            >>> pizarra.dibujar_punto(20, 30, pilas.colores.rojo)

        :param x: Posición horizontal para el punto.
        :param y: Posición vertical para el punto.
        :param color: El color para el punto.
        """

        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.dibujar_punto(x, y, color=color)

    def obtener_coordenada_fisica(self, x, y):
        """Convierte las coordenadas de pantalla a coordenadas físicas.

        Una coordenanda de pantalla, comienza en el punto (0, 0) y corresponde
        al centro de la pizarra. Mientras que una coordenada física tiene un
        sistema parecido al de los juegos viejos, donde (0, 0) es la esquina
        superir izquierda de la pantalla.

        :param x: Coordenada x a convertir.
        :param y: Coordenada y a convertir.
        """
        x = (self.imagen.ancho()/2) + x
        y = (self.imagen.alto()/2) - y
        return x, y

    def pintar_imagen(self, imagen, x, y):
        """Dibuja una imagen sobre la pizarra.

        :param imagen: Referencia a la imagen que se quiere pintar.
        :param x: Coordenada destino horizontal.
        :param y: Coordenada destino vertical.
        """
        self.pintar_parte_de_imagen(imagen, 0, 0, imagen.ancho(), imagen.alto(), x, y)

    def pintar_parte_de_imagen(self, imagen, origen_x, origen_y, ancho, alto, x, y):
        """Dibuja una porción de una imagen sobre la pizarra.

        Este método, a diferencia de "pintar_imagen", capturará un rectángulo
        de la imagen fuente.

        :param imagen: Imagen fuente que se quiere dibujar sobre la pizarra.
        :param origen_x: Marca la esquina superior izquierda desde donde se recortar.
        :param origen_y: Marca la esquina superior izquierda desde donde se recortar.
        :param ancho: Ancho del rectángulo de corte.
        :param alto: Alto del rectángulo de corte.
        """
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.pintar_parte_de_imagen(imagen, origen_x, origen_y, ancho, alto, x, y)

    def pintar_grilla(self, grilla, x, y):
        """Dibuja un cuadro de animación sobre la pizarra.

        :param grilla: La grilla a dibujar.
        :param x: Coordenada horizontal sobre la pizarra.
        :param y: Coordenada vertical sobre la pizarra.
        """
        grilla.dibujarse_sobre_una_pizarra(self, x, y)

    def pintar(self, color):
        """Pinta toda la pizarra de un solo color.

        Por ejemplo:

            >>> pizarra.pintar(pilas.colores.rojo)

        :param color: El color que pintará toda la pizarra.
        """
        self.imagen.pintar(color)

    def linea(self, x, y, x2, y2, color=colores.negro, grosor=1):
        """Dibuja una linea recta sobre la pizarra.

        :param x: Coordenada horizontal desde donde comenzará la linea.
        :param y: Coordenada vertical desde donde comenzará la linea.
        :param x2: Coordenada horizontal desde donde terminará la linea.
        :param y2: Coordenada vertical desde donde terminará la linea.
        :param color: El color de la linea.
        :param grosor: Cuan gruesa será la linea en pixels.
        """
        x, y = self.obtener_coordenada_fisica(x, y)
        x2, y2 = self.obtener_coordenada_fisica(x2, y2)
        self.imagen.linea(x, y, x2, y2, color, grosor)

    def rectangulo(self, x, y, ancho, alto, color=colores.negro, relleno=False, grosor=1):
        """Dibuja un rectángulo sobre la pizarra.

        Si el rectángulo se dibuja con relleno, el color será el que pintará todo
        el rectángulo, en caso contrario, el color será utilizado para dibujar el
        contorno del rectángulo.

        :param x: Posición horizontal de la esquina superior izquierda.
        :param y: Posición horizontal de la esquina superior izquierda.
        :param ancho: Ancho del rectángulo.
        :param alto: Altura del rectángulo.
        :param relleno: Indica con True o False si el rectángulo se tiene que pintar completamente.
        :param grosor: Grosor del contorno del rectángulogulo.
        """
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.rectangulo(x, y, ancho, alto, color, relleno, grosor)

    def texto(self, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro):
        """Dibuja una cadena de texto sobre la pizarra.

        :param cadena: El string que se quiere dibujar.
        :param x: Coordenada horizontal.
        :param y: Coordenada vertical.
        :param magnitud: Tamaño que tendrá la tipografía.
        :param fuente: Nombre de la tipografía a utilizar.
        :param color: Color del texto a dibujar.
        """
        x, y = self.obtener_coordenada_fisica(x, y)
        self.imagen.texto(cadena, x, y, magnitud, fuente, color)

    def poligono(self, puntos, color=pilas.colores.negro, grosor=1):
        """Dibuja un polígono sobre la pizarra.

        Ejemplo:

            >>> pizarra = pilas.actores.Pizarra()
            >>> pizarra.poligono([(10, 20), (100, 140)], color=pilas.colores.verde, grosor=4)

        :param puntos: Una lista de puntos en forma de tupla (x, y) que conforman el polígono.
        :param color: El color de la linea a trazar.
        :param grosor: El grosor de la linea a trazar en pixels.
        """
        puntos = [self.obtener_coordenada_fisica(*p) for p in puntos]
        self.imagen.poligono(puntos, color, grosor)

    def limpiar(self):
        """Borra toda la pizarra y los dibujos que hay en ella."""
        self.imagen.limpiar()
