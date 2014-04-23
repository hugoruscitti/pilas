# -*- encoding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from pilasengine.imagenes.imagen import Imagen
from pilasengine import colores

class Superficie(Imagen):

    def __init__(self, pilas, ancho, alto):
        self.pilas = pilas
        self._imagen = QtGui.QPixmap(ancho, alto)
        self._imagen.fill(QtGui.QColor(255, 255, 255, 0))
        self.canvas = QtGui.QPainter()
        self.ruta_original = os.urandom(25)

    def pintar(self, color):
        r, g, b, a = color.obtener_componentes()
        self._imagen.fill(QtGui.QColor(r, g, b, a))

    def pintar_parte_de_imagen(self, imagen, origen_x, origen_y, ancho, alto, x, y):
        self.canvas.begin(self._imagen)
        self.canvas.drawPixmap(x, y, imagen._imagen, origen_x, origen_y, ancho, alto)
        self.canvas.end()

    def pintar_imagen(self, imagen, x=0, y=0):
        self.pintar_parte_de_imagen(imagen, 0, 0, imagen.ancho(), imagen.alto(), x, y)

    def texto(self, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro, ancho=0, vertical=False):
        self.canvas.begin(self._imagen)
        r, g, b, _ = color.obtener_componentes()
        self.canvas.setPen(QtGui.QColor(r, g, b))
        dx = x
        dy = y

        #if fuente:
        #    nombre_de_fuente = Texto.cargar_fuente_desde_cache(fuente)
        #else:
        #    nombre_de_fuente = self.canvas.font().family()
        nombre_de_fuente = self.canvas.font().family()

        if not ancho:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
            ancho = self._imagen.width()
        else:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop

        font = QtGui.QFont(nombre_de_fuente, magnitud)
        self.canvas.setFont(font)

        if vertical:
            lineas = [t for t in cadena]
        else:
            lineas = cadena.split('\n')

        for line in lineas:
            r = QtCore.QRect(dx, dy, ancho, 2000)
            rect = self.canvas.drawText(r, flags, line)
            dy += rect.height()

        self.canvas.end()

    def circulo(self, x, y, radio, color=colores.negro, relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, _ = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        if relleno:
            self.canvas.setBrush(color)

        self.canvas.drawEllipse(x-radio, y-radio, radio*2, radio*2)
        self.canvas.end()

    def rectangulo(self, x, y, ancho, alto, color=colores.negro, relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, _ = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        if relleno:
            self.canvas.setBrush(color)

        self.canvas.drawRect(x, y, ancho, alto)
        self.canvas.end()

    def linea(self, x, y, x2, y2, color=colores.negro, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, _ = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        self.canvas.drawLine(x, y, x2, y2)
        self.canvas.end()

    def poligono(self, puntos, color, grosor, cerrado=False):
        x, y = puntos[0]

        if cerrado:
            puntos.append((x, y))

        for p in puntos[1:]:
            nuevo_x, nuevo_y = p
            self.linea(x, y, nuevo_x, nuevo_y, color, grosor)
            x, y = nuevo_x, nuevo_y

    def dibujar_punto(self, x, y, color=colores.negro):
        self.circulo(x, y, 3, color=color, relleno=True)

    def limpiar(self):
        self._imagen.fill(QtGui.QColor(0, 0, 0, 0))