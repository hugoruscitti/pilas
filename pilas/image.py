# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os

from PySFML import sf

import pilas

def load(path):
    """Intenta cargar la imagen indicada por el argumento ``path``.

    Por ejemplo::

        import pilas

        imagen = pilas.image.load("mi_archivo.png")

    En caso de éxito retorna el objeto Image, que se puede asignar
    a un Actor.

    El directorio de búsqueda de la imagen sigue el siguiente orden:

        * primero busca en el directorio actual.
        * luego en 'data'.
        * por último en el directorio estándar de la biblioteca.

    En caso de error genera una excepción de tipo IOError.
    """

    path = get_file_path(path)

    # Genera el objeto image y lo retorna.
    image = sf.Image()
    image.LoadFromFile(path)

    return image


def get_file_path(path):
    """Busca la ruta a un archivo de recursos.

    Los archivos de recursos (como las imagenes) se buscan en varios
    directorios (ver docstring de image.load), así que esta
    función intentará dar con el archivo en cuestión.
    """

    dirs = ['./', 'data', pilas.path, pilas.path + '/data']

    for x in dirs:
        full_path = os.path.join(x, path)
        #DEBUG: print "buscando en: '%s'" %(full_path)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." %(path))
