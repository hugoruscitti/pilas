# -*- encoding: utf-8 -*-
import os
from PyQt4 import QtGui

class Imagenes(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def cargar(self, ruta_a_imagen):
        ruta_a_imagen = self.pilas.obtener_ruta_al_recurso(ruta_a_imagen)
        return Imagen(ruta_a_imagen, self.pilas)

class Imagen(object):

    def __init__(self, ruta, pilas):
        self.ruta_original = ruta
        self.pilas = pilas

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

    def dibujar(self, painter, x, y, dx=0, dy=0, escala_x=1, escala_y=1, rotacion=0, transparencia=0):
        """Dibuja la imagen sobre la ventana que muestra el motor.

           x, y: indican la posicion dentro del mundo.
           dx, dy: es el punto centro de la imagen (importante para rotaciones).
           escala_x, escala_yindican cambio de tamano (1 significa normal).
           rotacion: angulo de inclinacion en sentido de las agujas del reloj.
        """

        painter.save()
        centro_x, centro_y = self.pilas.obtener_centro_fisico()
        painter.translate(x + centro_x, centro_y - y)
        painter.rotate(rotacion)
        painter.scale(escala_x, escala_y)

        if transparencia:
            painter.setOpacity(1 - transparencia/100.0)

        self._dibujar_pixmap(painter, -dx, -dy)
        painter.restore()

    def _dibujar_pixmap(self, painter, x, y):
        painter.drawPixmap(x, y, self._imagen)

    def __str__(self):
        nombre_imagen = os.path.basename(self.ruta_original)
        return "<Imagen del archivo '%s'>" % (nombre_imagen)