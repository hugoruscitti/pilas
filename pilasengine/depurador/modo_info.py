# -*- encoding: utf-8 -*-

import sys
import pilasengine
from pilasengine.depurador.modo import ModoDepurador

class ModoInformacionDeSistema(ModoDepurador):
    tecla = "F7"

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

        if pilas.usa_aceleracion():
            usa_aceleracion = "Sí"
        else:
            usa_aceleracion = "No"

        self.informacion = [
            "Usa aceleración de video: " + usa_aceleracion,
            "Sistema: " + sys.platform,
            "Version de pilas: " + pilasengine.VERSION,
            "Version de python: " + sys.subversion[0] + " " + sys.subversion[1],
            #"Version de Box2D: {}".format(pilas.fisica.obtener_version()),
            ]

    def termina_dibujado(self, motor, painter, lienzo):
        izquierda, derecha, arriba, abajo = 100, 300, 200, -200
        #pilas.utils.obtener_bordes()

        for (i, texto) in enumerate(self.informacion):
            posicion_y = abajo + 90 + i * 20
            lienzo.texto(painter, texto, izquierda + 10, posicion_y, color=pilas.colores.blanco)