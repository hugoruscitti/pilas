# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from pilasengine.colores import blanco


class Texto(Actor):

    def __init__(self, pilas, texto="Sin texto", magnitud=20, vertical=False,
                 fuente=None, fijo=True, ancho=0, x=0, y=0):
        """Inicializa el actor.

        :param texto: Texto a mostrar.
        :param magnitud: Tamaño del texto.
        :param vertical: Si el texto será vertical u horizontal,
                         como True o False.
        :param fuente: Nombre de la fuente a utilizar.
        :param fijo: Determina si el texto se queda fijo aunque se mueva
                     la camara. Por defecto está fijo.
        :param ancho: El limite horizontal en pixeles para la cadena, el texto
                      se mostrara en varias lineas si no cabe en este límite.
        """
        self._ancho = ancho
        self.__magnitud = magnitud
        self.__vertical = vertical
        self.__fuente = fuente
        self.__color = blanco
        Actor.__init__(self, pilas)
        self.x = x
        self.y = y
        self.centro = ("centro", "centro")
        self.fijo = fijo
        self.texto = texto

    def iniciar(self):
        pass

    def actualizar(self):
        pass

    def obtener_texto(self):
        """Retorna el texto definido."""
        return self.imagen.texto

    def definir_texto(self, texto):
        """Define el texto a mostrar."""
        imagen = self.pilas.imagenes.crear_texto(texto,
                                                 self.__magnitud,
                                                 self.__vertical,
                                                 self.__fuente,
                                                 color=self.__color,
                                                 ancho=self._ancho)

        if not self._ancho:
            self._ancho = imagen.ancho()

        self.imagen = imagen
        self.centro = ("centro", "centro")
        self.__texto = texto

    texto = property(obtener_texto, definir_texto,
                     doc="El texto que se tiene que mostrar.")


    def obtener_ancho(self):
        return self._ancho

    def definir_ancho(self, ancho):
        self._ancho = ancho
        self.definir_texto(self.texto)

    ancho = property(obtener_ancho, definir_ancho)

    def obtener_color(self):
        return self.__color

    def definir_color(self, color):
        self.__color = color
        # Actualiza el texto para forzar el re-dibujado
        self.texto = self.texto

    color = property(obtener_color, definir_color)
