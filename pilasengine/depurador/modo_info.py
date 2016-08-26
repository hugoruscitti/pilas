# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import sys


import pilasengine
from pilasengine.depurador.modo import ModoDepurador


class ModoInformacionDeSistema(ModoDepurador):
    tecla = "F7"

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

        usa_aceleracion = self._usa_aceleracion_de_video()

        self.informacion = [
            u"Usa aceleración de video: %s" % (usa_aceleracion),
            "Sistema: " + sys.platform,
            "Version de pilas: " + pilasengine.VERSION,
            "Version de python: " + sys.subversion[0] + " " + sys.subversion[1],
            "", # Interpolaciones en curso
            "", # Area de juego
            "", # Posición de la cámara
            "", # Rendimiento
            ""  # Cantidad de actores
        ]

    def _usa_aceleracion_de_video(self):
        return u"Sí" if self.pilas.usa_aceleracion() else u"No"

    def realizar_dibujado(self, painter):
        izquierda, derecha, _, abajo = self.pilas.widget.obtener_bordes()
        interpolaciones = self.pilas.utils.obtener_cantidad_de_interpolaciones()

        ancho, alto = self.pilas.obtener_area()
        self.informacion[4] = "Interpolaciones en curso: %d" %(interpolaciones)
        self.informacion[5] = "Area de juego: (%d, %d)" % (ancho, alto)
        self.informacion[6] = u"Posición de la cámara: (%d, %d)" % (self.pilas.camara.x, self.pilas.camara.y)
        self.informacion[7] = u"Rendimiento: %s cuadros por segundo" % (self.pilas.widget.fps.obtener_cuadros_por_segundo())
        self.informacion[8] = u"Cantidad de actores: %d" % (self.pilas.escena_actual().obtener_cantidad_de_actores())

        for (i, texto) in enumerate(self.informacion[::-1]):
            posicion_y = abajo + 20 + i * 20
            self._texto_absoluto(painter, texto, izquierda + 11, posicion_y - 1, color=pilasengine.colores.negro)
            self._texto_absoluto(painter, texto, izquierda + 10, posicion_y, color=pilasengine.colores.blanco)

        texto = u"Posición del mouse: (%d, %d)" %(self.pilas.obtener_posicion_del_mouse())
        self._texto_absoluto(painter, texto, derecha-9, abajo+7, color=pilasengine.colores.negro, alineado_a_derecha=True)
        self._texto_absoluto(painter, texto, derecha-10, abajo+8, color=pilasengine.colores.blanco, alineado_a_derecha=True)

    def dibujar_actor(self, actor, painter):
        pass
