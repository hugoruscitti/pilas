# -*- encoding: utf-8 -*-
import sys


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
        izquierda, _, _, abajo = self.pilas.widget.obtener_bordes()

        for (i, texto) in enumerate(self.informacion):
            posicion_y = abajo + 90 + i * 20
            self._texto(painter, texto, izquierda + 10, posicion_y, color=pilasengine.colores.blanco)

    def dibujar_actor(self, actor, painter):
        pass