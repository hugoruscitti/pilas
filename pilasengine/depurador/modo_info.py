# -*- encoding: utf-8 -*-
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from pilasengine.colores import negro
import pilasengine
from pilasengine.depurador.modo import ModoDepurador


class ModoInformacionDeSistema(ModoDepurador):
    tecla = "F7"

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

        if pilas.usa_aceleracion():
            usa_aceleracion = u"Sí"
        else:
            usa_aceleracion = u"No"

        self.informacion = [
            u"Usa aceleración de video: %s" %(usa_aceleracion),
            "Sistema: " + sys.platform,
            "Version de pilas: " + pilasengine.VERSION,
            "Version de python: " + sys.subversion[0] + " " + sys.subversion[1],
            #"Version de Box2D: {}".format(pilas.fisica.obtener_version()),
            ]

    def realizar_dibujado(self, painter):
        izquierda, derecha, arriba, abajo = self.pilas.widget.obtener_bordes()

        for (i, texto) in enumerate(self.informacion):
            posicion_y = abajo + 90 + i * 20
            self.texto(painter, texto, izquierda + 10, posicion_y, color=pilasengine.colores.blanco)

    def dibujar_actor(self, actor, painter):
        pass

    def texto(self, painter, cadena, x=0, y=0, magnitud=10, fuente=None, color=negro):
        "Imprime un texto respespetando el desplazamiento de la camara."
        self.texto_absoluto(painter, cadena, x, y, magnitud, fuente, color)

    def texto_absoluto(self, painter, cadena, x=0, y=0, magnitud=10, fuente=None, color=negro):
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