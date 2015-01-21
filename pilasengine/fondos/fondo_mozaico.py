# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.fondos.fondo import Fondo


class FondoMozaico(Fondo):

    def __init__(self, pilas=None, imagen=None):
        super(FondoMozaico, self).__init__(pilas, imagen)

    def dibujar(self, painter):
        painter.save()

        x = self.pilas.obtener_escena_actual().camara.x
        y = -self.pilas.obtener_escena_actual().camara.y

        ancho, alto = self.pilas.obtener_area()
        painter.drawTiledPixmap(-ancho/2, -alto/2, ancho, alto,
                                self.imagen._imagen,
                                x % self.imagen.ancho(), 
                                y % self.imagen.alto())

        painter.restore()
        