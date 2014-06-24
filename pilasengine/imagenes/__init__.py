# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
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

    cargar_superficie = crear_superficie

    def crear_texto(self, cadena_de_texto, magnitud, vertical, fuente,
                    color, ancho):
        import texto
        return texto.Texto(self.pilas, cadena_de_texto, magnitud, vertical,
                           fuente, color, ancho)

    def cargar_grilla(self, ruta, columnas=1, filas=1):
        """Representa una grilla de imagenes con varios cuadros de animación.

        Una grilla es un objeto que se tiene que inicializar con la ruta
        a una imagen, la cantidad de columnas y filas.

        Por ejemplo, si tenemos una grilla con 2 columnas y 3 filas
        podemos asociarla a un actor de la siguiente manera::

            grilla = pilas.imagenes.cargar_grilla("animacion.png", 2, 3)
            grilla.asignar(actor)

        Entonces, a partir de ahora nuestro actor muestra solamente un
        cuadro de toda la grilla.

        Si quieres avanzar la animacion tienes que modificar el objeto
        grilla y asignarlo nuevamente al actor::

            grilla.avanzar()
            grilla.asignar(actor)
        """
        import grilla
        ruta_a_imagen = self.pilas.obtener_ruta_al_recurso(ruta)
        return grilla.Grilla(self.pilas, ruta_a_imagen, columnas, filas)

    def cargar_animacion(self, ruta, columnas=1, filas=1):
        import animacion
        ruta_a_imagen = self.pilas.obtener_ruta_al_recurso(ruta)
        return animacion.Animacion(self.pilas, ruta_a_imagen, columnas, filas)
