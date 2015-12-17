# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.fondos import fondo


class DesplazamientoHorizontal(fondo.Fondo):
    """
    Representa un fondo con desplazamiento horizontal y repetido.

    Este tipo de fondo es ideal para animaciones y juegos donde
    el fondo se puede repetir una y otra vez. Por ejemplo en un juego
    de carreras horizontal o de naves.

    El fondo inicialmente no tiene apariencia, pero se pueden agregar
    capas, cada una con su propia velocidad y posición.

    Por ejemplo, si queremos simular un fondo con 3 capas, una lejana
    con estrellas, y luego dos capas mas cercanas con arboles y arbustos
    podemos escribir:

        >>> fondo = pilas.fondos.DesplazamientoHorizontal()
        >>> fondo.agregar("estrellas.png", 0, 0, 0)
        >>> fondo.agregar("arboles_lejanos.png", 0, 0, 1)
        >>> fondo.agregar("arbustos_cercanos.png", 0, 0, 2)

    El primer argumento del método agregar es la imagen que se tiene
    que repetir horizontalmente. Luego viene la posición 'x' e 'y'. Por
    último el valor numérico es la velocidad de movimiento que tendría
    esa capa.

    Un valor grande de velocidad significa que la capa se moverá
    mas rápido que otras ante un cambio de posición en la cámara. Por
    ejemplo, la capa que tiene velocidad 2 significa que se moverá 2 pixels
    hacia la izquierda cada vez que la cámara mire 2 pixel hacia la derecha.

    Si la capa tiene velocidad 0 significa que permanecerá inamovible al movimiento
    de la cámara.
    """

    def iniciar(self):
        self.capas = []
        self.imagen = "invisible.png"
        self.pilas.eventos.mueve_camara.conectar(self.cuando_mueve_camara)
        self.z = 1000

    def dibujar(self, painter):
        painter.save()
        ancho, alto = self.pilas.widget.obtener_area()

        for capa in self.capas:
            capa.dibujar_tiled_horizontal(painter, ancho, alto)

        painter.restore()

    def agregar(self, imagen, x=0, y=0, velocidad=1):
        nueva_capa = Capa(self.pilas, imagen, x, y, velocidad)
        nueva_capa.z = self.z
        self.capas.append(nueva_capa)

    def cuando_mueve_camara(self, evento):
        for capa in self.capas:
            capa.mover_horizontal(evento.dx)

    def esta_fuera_de_la_pantalla(self):
        return False

    def desplazar(self, dx):
        for capa in self.capas:
            capa.mover_horizontal(dx)



class Capa(object):

    def __init__(self, pilas, imagen, x, y, velocidad):
        self.imagen = pilas.imagenes.cargar(imagen)
        self.x = x
        self.y = y
        self.velocidad = velocidad

    def dibujar_tiled_horizontal(self, painter, ancho, alto):
        dx = self.x % self.imagen.ancho()
        dy = 0
        x_inicial = - ancho / 2
        y_inicial = - self.imagen.alto() / 2
        painter.drawTiledPixmap(x_inicial, y_inicial + self.y, ancho, self.imagen.alto(), self.imagen._imagen,
                                abs(dx) % self.imagen.ancho(), dy % self.imagen.alto())

    def mover_horizontal(self, dx):
        self.x += dx * self.velocidad
