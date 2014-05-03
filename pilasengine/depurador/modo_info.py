# -*- encoding: utf-8 -*-
import sys


import pilasengine
from pilasengine.depurador.modo import ModoDepurador


class ModoInformacionDeSistema(ModoDepurador):
    tecla = "F7"

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

        usa_aceleracion = self._usa_aceleracion_de_video(pilas)

        self.informacion = [
            u"Usa aceleración de video: %s" %(usa_aceleracion),
            "Sistema: " + sys.platform,
            "Version de pilas: " + pilasengine.VERSION,
            "Version de python: " + sys.subversion[0] + " " + sys.subversion[1],
            "",
            "",
        ]

    def _usa_aceleracion_de_video(self, pilas):
        if pilas.usa_aceleracion():
            usa_aceleracion = u"Sí"
        else:
            usa_aceleracion = u"No"
        return usa_aceleracion

    def realizar_dibujado(self, painter):
        izquierda, _, _, abajo = self.pilas.widget.obtener_bordes()

        ancho, alto = self.pilas.obtener_area()
        self.informacion[4] = "Area de juego: (%d, %d)" %(ancho, alto)
        self.informacion[5] = u"Posición de la cámara: (%d, %d)" %(self.pilas.camara.x, self.pilas.camara.y)

        for (i, texto) in enumerate(self.informacion[::-1]):
            posicion_y = abajo + 90 + i * 20
            self._texto(painter, texto, izquierda + 10, posicion_y, color=pilasengine.colores.blanco)

    def dibujar_actor(self, actor, painter):
        pass