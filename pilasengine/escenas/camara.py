# -*- encoding: utf -*-
class Camara(object):

    def __init__(self, pilas, escena):
        self.pilas = pilas
        self.escena = escena
        self.x = 0
        self.y = 0
        self.zoom = 1

    def aplicar_transformaciones(self, painter):
        painter.scale(self.zoom, self.zoom)