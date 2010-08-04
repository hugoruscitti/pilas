# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os

from PySFML import sf

def load(path):
    """Intenta cargar la imagen indicada por el argumento ``path``.

    Por ejemplo::

        import pilas

        imagen = pilas.image.load("mi_archivo.png")

    
    En caso de éxito retorna el objeto Image, que se puede asignar
    a un Actor.

    En caso de error genera una excepción de tipo IOError.
    """

    if not os.path.exists(path):
        raise IOError("El archivo '%s' no existe." %(path))

    image = sf.Image()
    image.LoadFromFile(path)

    return image
