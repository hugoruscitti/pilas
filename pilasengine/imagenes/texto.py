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
from pilasengine.imagenes.superficie import Superficie

class Texto(Superficie):
    CACHE_FUENTES = {}

    def __init__(self, pilas, texto, magnitud, vertical, fuente, color, ancho):
        ancho, alto = self._obtener_area_de_texto(texto, magnitud, vertical, fuente, ancho)
        Superficie.__init__(self, pilas, ancho, alto)
        self._ancho_del_texto = ancho
        self.dibujar_texto = self.texto
        self.dibujar_texto(texto, magnitud=magnitud, fuente=fuente, color=color, ancho=ancho, vertical=vertical)
        self.ruta_original = texto.encode('ascii', 'xmlcharrefreplace') + str(os.urandom(25))
        self.texto = texto

    def _obtener_area_de_texto(self, cadena, magnitud=10, vertical=False, fuente=None, ancho=0):
        pic = QtGui.QPicture()
        p = QtGui.QPainter(pic)

        if fuente:
            nombre_de_fuente = Texto.cargar_fuente_desde_cache(fuente)
        else:
            nombre_de_fuente = p.font().family()

        font = QtGui.QFont(nombre_de_fuente, magnitud)
        p.setFont(font)

        alto = 0

        if vertical:
            lineas = [t for t in cadena]
        else:
            lineas = cadena.split('\n')

        if not ancho:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        else:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop

        for line in lineas:
            if line == '':
                line = ' '

            brect = p.drawText(QtCore.QRect(0, 0, ancho, 2000), flags, line)
            ancho = max(ancho, brect.width())
            alto += brect.height()

        p.end()
        return (ancho, alto)


    @classmethod
    def cargar_fuente_desde_cache(kclass, fuente_como_ruta):
        """Carga o convierte una fuente para ser utilizada dentro del motor.

        Permite a los usuarios referirse a las fuentes como ruta a archivos, sin
        tener que preocuparse por el font-family.

        :param fuente_como_ruta: Ruta al archivo TTF que se quiere utilizar.

        Ejemplo:

            >>> Texto.cargar_fuente_desde_cache('myttffile.ttf')
            'Visitor TTF1'
        """

        if not fuente_como_ruta in Texto.CACHE_FUENTES.keys():
            ruta_a_la_fuente = self.pilas.obtener_ruta_al_recurso(fuente_como_ruta)
            fuente_id = QtGui.QFontDatabase.addApplicationFont(ruta_a_la_fuente)
            Texto.CACHE_FUENTES[fuente_como_ruta] = fuente_id
        else:
            fuente_id = Texto.CACHE_FUENTES[fuente_como_ruta]

        return str(QtGui.QFontDatabase.applicationFontFamilies(fuente_id)[0])
