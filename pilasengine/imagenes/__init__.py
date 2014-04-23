# -*- encoding: utf-8 -*-
import os
from PyQt4 import QtGui
import pilasengine

class Imagenes(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def cargar(self, ruta_a_imagen):
        import imagen
        ruta_a_imagen = self.pilas.obtener_ruta_al_recurso(ruta_a_imagen)
        return imagen.Imagen(self.pilas, ruta_a_imagen)

    def crear_superficie(self, ancho, alto):
        import superficie
        return superficie.Superficie(self.pilas, ancho, alto)

    def crear_texto(self, cadena_de_texto, magnitud, vertical, fuente, color, ancho):
        import texto
        return texto.Texto(self.pilas, cadena_de_texto, magnitud, vertical, fuente, color, ancho)