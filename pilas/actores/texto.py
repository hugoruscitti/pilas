# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from .actor import Actor

class Texto(Actor):
    """Representa un texto en pantalla.

    El texto tiene atributos como ``texto``, ``magnitud`` y ``color``, por
    ejemplo para crear un mensaje de saludo podríamos escribir:

        >>> saludo = pilas.actores.Texto("Hola mundo!")
    """

    def __init__(self, texto="None", x=0, y=0, magnitud=20, vertical=False, fuente=None, fijo=True, ancho=0):
        """Inicializa el actor.

        :param texto: Texto a mostrar.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param magnitud: Tamaño del texto.
        :param vertical: Si el texto será vertical u horizontal, como True o False.
        :param fuente: Nombre de la fuente a utilizar.
        :param fijo: Determina si el texto se queda fijo aunque se mueva la camara. Por defecto está fijo.
        :param ancho: El limite horizontal en pixeles para la cadena, el texto de mostrara en varias lineas si no cabe en este límite.
        """
        self._ancho_del_texto = ancho
        self.__magnitud = magnitud
        self.__vertical = vertical
        self.__fuente = fuente
        self.__color = pilas.colores.blanco
        Actor.__init__(self, x=x, y=y)
        self.centro = ("centro", "centro")
        self.fijo = fijo
        self.texto = texto

    def obtener_texto(self):
        """Retorna el texto definido."""
        return self.imagen.texto

    def definir_texto(self, texto):
        """Define el texto a mostrar."""
        imagen = pilas.mundo.motor.obtener_texto(texto, self.__magnitud, self.__vertical, self.__fuente, color=self.__color, ancho=self._ancho_del_texto)

        if not self._ancho_del_texto:
            self._ancho_del_texto = imagen.ancho()

        self.imagen = imagen
        self.centro = ("centro", "centro")
        self.__texto = texto

    texto = property(obtener_texto, definir_texto, doc="El texto que se tiene que mostrar.")

    def obtener_magnitud(self):
        """Devuelve el tamaño del texto."""
        return self.__magnitud

    def definir_magnitud(self, magnitud):
        """Define el tamaño del texto a mostrar."""
        self.__magnitud = magnitud
        self.definir_texto(self.__texto)

    magnitud = property(obtener_magnitud, definir_magnitud, doc="El tamaño del texto.")

    def obtener_color(self):
        """Devuelve el color que tiene asignado el texto."""
        return self.__color

    def definir_color(self, color):
        """Define el color del texto."""
        self.__color = color
        self.definir_texto(self.__texto)

    color = property(obtener_color, definir_color, doc="Color del texto.")

    def obtener_ancho(self):
        return self._ancho_del_texto

    def definir_ancho(self, ancho):
        self._ancho_del_texto = ancho
        self.texto = self.texto

    ancho = property(obtener_ancho, definir_ancho, doc="Ancho del texto a mostrar")
