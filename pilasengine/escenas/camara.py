# -*- encoding: utf -*-
class Camara(object):

    def __init__(self, pilas, escena):
        self.pilas = pilas
        self.escena = escena
        self._x = 0
        self._y = 0
        self._aumento = 1
        self._rotacion = 0

    def aplicar_transformaciones_completas(self, painter):
        centro_x, centro_y = self.pilas.obtener_centro_fisico()
        painter.translate(centro_x, centro_y)
        painter.scale(self._aumento, self._aumento)
        painter.rotate(-self._rotacion)

    def aplicar_translacion(self, painter):
        centro_x, centro_y = self.pilas.obtener_centro_fisico()
        painter.translate(centro_x, centro_y)

    def obtener_aumento(self):
        return self._aumento

    def definir_aumento(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'aumento', valor)

    def obtener_rotacion(self):
        return self._rotacion

    def definir_rotacion(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'rotacion', valor)

    def obtener_x(self):
        return self._x

    def definir_x(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'x', valor)

    def obtener_y(self):
        return self._y

    def definir_y(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'y', valor)

    aumento = property(obtener_aumento, definir_aumento, doc="Cambia el aumento o cercanía de la cámara.")
    rotacion = property(obtener_rotacion, definir_rotacion, doc="Cambia la rotacion de la pantalla.")
    x = property(obtener_x, definir_x, doc="Cambia la posición x de la pantalla.")
    y = property(obtener_y, definir_y, doc="Cambia la posición y de la pantalla.")