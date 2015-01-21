# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.fondos import fondo


class Color(fondo.Fondo):

    def __init__(self, pilas, color):
        fondo.Fondo.__init__(self, pilas)
        (ancho, alto) = self.pilas.obtener_area()
        self.imagen = self.pilas.imagenes.crear_superficie(ancho, alto)
        self.imagen.pintar(color)
