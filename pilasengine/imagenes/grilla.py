# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os

from imagen import Imagen


class Grilla(Imagen):

    """Representa una grilla regular, que se utiliza en animaciones.

       La grilla regular se tiene que crear indicando la cantidad
       de filas y columnas. Una vez definida se puede usar como
       una imagen normal, solo que tiene dos metodos adicionales
       para ``definir_cuadro`` y ``avanzar`` el cuadro actual.
    """

    def __init__(self, pilas, ruta, columnas=1, filas=1):
        Imagen.__init__(self, pilas, ruta)
        self.cantidad_de_cuadros = columnas * filas
        self.columnas = columnas
        self.filas = filas
        self.cuadro_ancho = Imagen.ancho(self) / columnas
        self.cuadro_alto = Imagen.alto(self) / filas
        self.definir_cuadro(0)

    def ancho(self):
        return self.cuadro_ancho

    def alto(self):
        return self.cuadro_alto

    def _dibujar_pixmap(self, painter):
        painter.drawPixmap(0, 0, self._imagen, self.dx, self.dy,
                           self.cuadro_ancho, self.cuadro_alto)

    def definir_cuadro(self, cuadro):
        self._ticks_acumulados = 0
        self._cuadro = cuadro

        frame_col = cuadro % self.columnas
        frame_row = cuadro / self.columnas

        self.dx = frame_col * self.cuadro_ancho
        self.dy = frame_row * self.cuadro_alto

    def avanzar(self, velocidad=60):
        velocidad_de_animacion = (1000.0 / 60) * velocidad
        self._ticks_acumulados += velocidad_de_animacion
        ha_avanzado = True

        if self._ticks_acumulados > 1000.0:
            self._ticks_acumulados -= 1000.0
            cuadro_actual = self._cuadro + 1

            if cuadro_actual >= self.cantidad_de_cuadros:
                cuadro_actual = 0
                ha_avanzado = False

            self.definir_cuadro(cuadro_actual)

        return ha_avanzado

    def obtener_cuadro(self):
        return self._cuadro

    def dibujarse_sobre_una_pizarra(self, pizarra, x, y):
        pizarra.pintar_parte_de_imagen(self, self.dx, self.dy,
                                       self.cuadro_ancho, self.cuadro_alto,
                                       x, y)

    def __repr__(self):
        nombre_imagen = os.path.basename(self.ruta_original)
        return "<Grilla del archivo '%s' (filas: %d, columnas: %d)>" % (nombre_imagen, self.filas, self.columnas)
