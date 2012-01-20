# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
import os


def cargar(ruta):
    """Carga un canción para reproducir, donde el argumento ``ruta`` indica cual es el archivo.

    Por ejemplo::

        import pilas

        risa = pilas.musica.cargar("jazz_loop.ogg")

    En caso de éxito retorna el objeto Musica, que se puede
    reproducir usando el método ``reproducir()``, por ejemplo::

        risa.reproducir(repetir=True)

    El directorio de búsqueda del sonido sigue el siguiente orden:

        * primero busca en el directorio actual.
        * luego en 'data'.
        * por último en el directorio estándar de la biblioteca.

    En caso de error genera una excepción de tipo IOError.
    """
    ruta = pilas.utils.obtener_ruta_al_recurso(ruta)
    return pilas.mundo.motor.cargar_musica(ruta)
