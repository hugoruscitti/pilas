# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.fondos.fondo import Fondo
from pilasengine.fondos.fondo_mozaico import FondoMozaico


class Galaxia(FondoMozaico):
    
    def iniciar(self):
        self.imagen = "fondos/galaxia.png"
        self.dx = 0
        self.dy = 0
        self.acumulador_x = 0
        self.acumulador_y = 0

    def dibujar(self, painter):
        painter.save()

        x = self.pilas.obtener_escena_actual().camara.x + self.acumulador_x
        y = -self.pilas.obtener_escena_actual().camara.y + self.acumulador_y

        ancho, alto = self.pilas.obtener_area()
        painter.drawTiledPixmap(-ancho/2, -alto/2, ancho, alto,
                                self.imagen._imagen,
                                x % self.imagen.ancho(), 
                                y % self.imagen.alto())

        painter.restore()
        
    def actualizar(self):
        self.acumulador_x += self.dx
        self.acumulador_y += self.dy