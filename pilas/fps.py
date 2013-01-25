# -*- encoding: utf-8 -*-
from PyQt4 import QtCore

class FPS(object):
    """Representa un controlador de tiempo para el mainloop de pilas."""

    def __init__(self, fps, usar_modo_economico):
        """Inicia el administrador de cuadros por segundo.

        :param fps: Cantidad de cuadros por segundo esperados.
        :param usar_modo_economico: Si vale True intenta reducir la cantidad de recursos utilizados.
        """
        # TODO: Eliminar el argumento usar_modo_economico que no se está usando.
        self.cuadros_por_segundo = "??"
        self.frecuencia = 1000.0 / fps
        self.timer = QtCore.QTime()
        self.timer.start()
        self.siguiente = self.timer.elapsed() + self.frecuencia
        self.cuadros = 0
        self.ultimo_reporte_fps = 0
        self.cuadros_por_segundo_numerico = 0

    def actualizar(self):
        actual = self.timer.elapsed()

        if actual > self.siguiente:
            cantidad = 0

            while actual > self.siguiente:
                self.siguiente += self.frecuencia
                cantidad += 1
                self._procesar_fps(actual)

            if cantidad > 10:
                cantidad = 10

            self.cuadros += 1
            return cantidad
        else:
            # wait
            return 0

    def _procesar_fps(self, actual):
        if actual - self.ultimo_reporte_fps > 1000.0:
            self.ultimo_reporte_fps += 1000.0
            self.cuadros_por_segundo = str(self.cuadros)
            self.cuadros_por_segundo_numerico = self.cuadros
            self.cuadros = 0

    def obtener_cuadros_por_segundo(self):
        "Retorna la cantidad de cuadros por segundo."
        return self.cuadros_por_segundo
