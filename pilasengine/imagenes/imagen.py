# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
from PyQt4 import QtGui


class Imagen(object):

    def __init__(self, pilas, ruta):
        self.ruta_original = ruta
        self.pilas = pilas
        self.repetir_horizontal = False
        self.repetir_vertical = False

        if isinstance(ruta, QtGui.QPixmap):
            self._imagen = ruta
        else:
            if ruta.lower().endswith("jpeg") or ruta.lower().endswith("jpg"):
                try:
                    self._imagen = self.cargar_jpeg(ruta)
                except:
                    self._imagen = QtGui.QPixmap(ruta)
            else:
                self._imagen = QtGui.QPixmap(ruta)

    def ancho(self):
        return self._imagen.size().width()

    def alto(self):
        return self._imagen.size().height()

    def centro(self):
        "Retorna una tupla con la coordenada del punto medio del la imagen."
        return (self.ancho()/2, self.alto()/2)

    def dibujar(self, painter, composicion):
        """Dibuja la imagen sobre la ventana que muestra el motor.

           x, y: indican la posicion dentro del mundo.
           dx, dy: es el punto centro de la imagen (importante para rotaciones).
           escala_x, escala_yindican cambio de tamano (1 significa normal).
           rotacion: angulo de inclinacion en sentido de las agujas del reloj.
        """
        if composicion:
            painter.setCompositionMode(composicion)
            self._dibujar_pixmap(painter)
        else:
            self._dibujar_pixmap(painter)

    def _dibujar_pixmap(self, painter):
        if self.repetir_horizontal or self.repetir_vertical:
            x = 0
            y = 0

            if self.repetir_horizontal:
                x = self.ancho() * 200

            if self.repetir_vertical:
                y = self.ancho() * 200

            painter.drawTiledPixmap(-x, -y, self.ancho() + x*2, self.alto() +y*2, self._imagen)
        else:
            painter.drawPixmap(0, 0, self._imagen)

    def __repr__(self):
        nombre_imagen = os.path.basename(self.ruta_original)
        return "<Imagen del archivo '%s'>" % (nombre_imagen)

    def definir_cuadro(self, cuadro):
        pass

    def avanzar(self, velocidad=60):
        pass