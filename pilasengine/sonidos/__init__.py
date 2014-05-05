# -*- encoding: utf-8 -*-
import os
import pilasengine
import sonido

class Sonidos(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def cargar(self, ruta):
        ruta_al_sonido = self.pilas.obtener_ruta_al_recurso(ruta)
        return sonido.Sonido(ruta_al_sonido)