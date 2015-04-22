# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from pilasengine.imagenes.imagen import Imagen
from pilasengine import colores
from pilasengine import utils


class Superficie(Imagen):
    CACHE_FUENTES = {}

    def __init__(self, pilas, ancho, alto):
        self.pilas = pilas
        self._imagen = QtGui.QPixmap(ancho, alto)
        self._imagen.fill(QtGui.QColor(255, 255, 255, 0))
        self.canvas = QtGui.QPainter()
        self.ruta_original = os.urandom(25)
        self.repetir_horizontal = False
        self.repetir_vertical = False

    def pintar(self, color):
        r, g, b, a = color.obtener_componentes()
        self._imagen.fill(QtGui.QColor(r, g, b, a))

    def pintar_parte_de_imagen(self, imagen, origen_x, origen_y, ancho, alto,
                               x, y):
        self.canvas.begin(self._imagen)
        self.canvas.drawPixmap(x, y, imagen._imagen, origen_x, origen_y,
                               ancho, alto)
        self.canvas.end()

    def pintar_imagen(self, imagen, x=0, y=0):
        self.pintar_parte_de_imagen(imagen, 0, 0, imagen.ancho(),
                                    imagen.alto(), x, y)

    def texto(self, cadena, x=0, y=0, magnitud=10, fuente=None,
              color=colores.negro, ancho=0, vertical=False):
        self.canvas.begin(self._imagen)
        color = colores.generar_color_desde_texto(color)
        r, g, b, _ = color.obtener_componentes()
        self.canvas.setPen(QtGui.QColor(r, g, b))
        dx = x
        dy = y

        if fuente:
            nombre_de_fuente = self.cargar_fuente(fuente)
        else:
            nombre_de_fuente = self.canvas.font().family()

        #nombre_de_fuente = self.canvas.font().family()

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

    def circulo(self, x, y, radio, color=colores.negro,
                relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, _ = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        if relleno:
            self.canvas.setBrush(color)

        self.canvas.drawEllipse(x-radio, y-radio, radio*2, radio*2)
        self.canvas.end()

    def rectangulo(self, x, y, ancho, alto, color=colores.negro,
                   relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b, a)
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

    def cargar_fuente(self, fuente_como_ruta):
        """Carga o convierte una fuente para ser utilizada dentro del motor.

        Permite a los usuarios referirse a las fuentes como ruta a archivos, sin
        tener que preocuparse por el font-family.

        :param fuente_como_ruta: Ruta al archivo TTF que se quiere utilizar.

        Ejemplo:

            >>> Texto.cargar_fuente('myttffile.ttf')
            'Visitor TTF1'
        """

        if not fuente_como_ruta in Superficie.CACHE_FUENTES.keys():
            ruta_a_la_fuente = utils.obtener_ruta_al_recurso(fuente_como_ruta)
            fuente_id = QtGui.QFontDatabase.addApplicationFont(ruta_a_la_fuente)
            Superficie.CACHE_FUENTES[fuente_como_ruta] = fuente_id
        else:
            fuente_id = Superficie.CACHE_FUENTES[fuente_como_ruta]

        return str(QtGui.QFontDatabase.applicationFontFamilies(fuente_id)[0])

    def __repr__(self):
        return "<Superficie>"
