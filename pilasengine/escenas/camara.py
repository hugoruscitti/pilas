# -*- encoding: utf -*-
class Camara(object):

    def __init__(self, pilas, escena):
        self.pilas = pilas
        self.escena = escena
        self.x = 0
        self.y = 0
        self.zoom = 2

    def aplicar_transformaciones(self, painter):
        centro_x, centro_y = self.pilas.obtener_centro_fisico()
        painter.translate(centro_x, centro_y)
        painter.scale(self.zoom, self.zoom)