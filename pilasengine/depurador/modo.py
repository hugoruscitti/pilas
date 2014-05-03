# -*- encoding: utf-8 -*-
from pilasengine.colores import negro
from PyQt4 import QtGui
from PyQt4 import QtCore

class ModoDepurador(object):
    tecla = "F00"

    def __init__(self, pilas, depurador):
        self.pilas = pilas
        self.depurador = depurador

    def realizar_dibujado(self, painter, lienzo):
        pass

    def dibuja_actor(self, painter, lienzo, actor):
        pass

    def termina_dibujado(self, painter, lienzo):
        pass

    def orden_de_tecla(self):
        return int(self.tecla[1:])

    def sale_del_modo(self):
        pass

    def _texto(self, painter, cadena, x=0, y=0, magnitud=12, fuente=None, color=negro):
        "Imprime un texto respespetando el desplazamiento de la camara."
        self._texto_absoluto(painter, cadena, x, y, magnitud, fuente, color)

    def _texto_absoluto(self, painter, cadena, x=0, y=0, magnitud=10, fuente=None, color=negro):
        "Imprime un texto sin respetar al camara."
        x, y = self.pilas.obtener_coordenada_de_pantalla_absoluta(x, y)

        r, g, b, _ = color.obtener_componentes()
        painter.setPen(QtGui.QColor(r, g, b))

        #if fuente:
        #    nombre_de_fuente = Texto.cargar_fuente_desde_cache(fuente)
        #else:
        #    nombre_de_fuente = painter.font().family()
        nombre_de_fuente = painter.font().family()

        font = QtGui.QFont(nombre_de_fuente, magnitud)
        painter.setFont(font)
        painter.drawText(x, y, cadena)