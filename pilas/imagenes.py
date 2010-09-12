# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PySFML import sf
import pilas
import os

def cargar(ruta):
    """Intenta cargar la imagen indicada por el argumento ``ruta``.

    Por ejemplo::

        import pilas

        imagen = pilas.imagenes.cargar("mi_archivo.png")

    En caso de éxito retorna el objeto Image, que se puede asignar
    a un Actor.

    El directorio de búsqueda de la imagen sigue el siguiente orden:

        * primero busca en el directorio actual.
        * luego en 'data'.
        * por último en el directorio estándar de la biblioteca.

    En caso de error genera una excepción de tipo IOError.
    """

    ruta = pilas.utils.obtener_ruta_al_recurso(ruta)

    # Genera el objeto image y lo retorna.
    image = sf.Image()
    image.LoadFromFile(ruta)

    return image


class Grilla:
    """Representa una grilla de imagenes con varios cuadros de animación.

    Una grilla es un objeto que se tiene que inicializar con la ruta
    a una imagen, la cantidad de columnas y filas.

    Por ejemplo, si tenemos una grilla con 2 columnas y 3 filas
    podemos asociarla a un actor de la siguiente manera::

        grilla = pilas.imagenes.Grilla("animacion.png", 2, 3)
        grilla.asignar(actor)

    Entonces, a partir de ahora nuestro actor muestra solamente un
    cuadro de toda la grilla.

    Si quieres avanzar la animacion tienes que modificar el objeto
    grilla y asignarlo nuevamente al actor::

        grilla.avanzar()
        grilla.asignar(actor)
    """

    def __init__(self, ruta, columnas=1, filas=1):
        self.image = pilas.imagenes.cargar(ruta)
        self.cantidad_de_cuadros = columnas * filas
        self.columnas = columnas
        self.filas = filas
        self.cuadro_ancho = self.image.GetWidth() / columnas
        self.cuadro_alto = self.image.GetHeight() / filas
        self.sub_rect = sf.IntRect(0, 0, self.cuadro_ancho, self.cuadro_alto)
        self.definir_cuadro(0)

    def definir_cuadro(self, cuadro):
        self.cuadro = cuadro

        frame_col = cuadro % self.columnas
        frame_row = cuadro / self.columnas

        dx = frame_col * self.cuadro_ancho - self.sub_rect.Left
        dy = frame_row * self.cuadro_alto - self.sub_rect.Top

        self.sub_rect.Offset(dx, dy)

    def asignar(self, sprite):
        "Sets the sprite's image with animation state."

        sprite.SetImage(self.image)
        sprite.SetSubRect(self.sub_rect)

    def avanzar(self):
        ha_reiniciado = False
        cuadro_actual = self.cuadro + 1

        if cuadro_actual >= self.cantidad_de_cuadros:
            cuadro_actual = 0
            ha_reiniciado = True

        self.definir_cuadro(cuadro_actual)
        return ha_reiniciado

    def obtener_cuadro(self):
        return self.cuadro
