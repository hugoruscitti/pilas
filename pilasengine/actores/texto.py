# -*- encoding: utf-8 -*-
from pilasengine.actores.actor import Actor
from pilasengine.colores import blanco

class Texto(Actor):

    def __init__(self, pilas, texto="Sin texto", magnitud=20, vertical=False,
              fuente=None, fijo=True, ancho=0):
        """Inicializa el actor.

        :param texto: Texto a mostrar.
        :param magnitud: Tamaño del texto.
        :param vertical: Si el texto será vertical u horizontal, como True o False.
        :param fuente: Nombre de la fuente a utilizar.
        :param fijo: Determina si el texto se queda fijo aunque se mueva la camara. Por defecto está fijo.
        :param ancho: El limite horizontal en pixeles para la cadena, el texto de mostrara en varias lineas si no cabe en este límite.
        """
        Actor.__init__(self, pilas)
        self._ancho = ancho
        self.__magnitud = magnitud
        self.__vertical = vertical
        self.__fuente = fuente
        self.__color = blanco
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

    texto = property(obtener_texto, definir_texto, doc="El texto que se tiene que mostrar.")