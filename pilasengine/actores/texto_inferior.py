# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.texto import Texto
from pilasengine.colores import blanco

class TextoInferior(Texto):
    """Representa un texto al pie de la ventana.

    Esta clase se utiliza desde el método "pilas.avisar()".
    """
    def __init__(self, pilas, texto="Sin texto", magnitud=20, vertical=False,
              fuente=None, fijo=True, ancho=0, x=0, y=0, retraso=5):
        """Inicializa el texto.

        :param texto: Texto a mostrar.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param magnitud: Tamaño del texto.
        :param vertical: Si el texto será vertical u horizontal, como True o False.
        """
        Texto.__init__(self, pilas, texto, magnitud)
        izquierda, _, _, abajo = self.obtener_bordes()

        self.z = -100
        TextoInferior.anterior_texto = self

        self.centro = ("centro", "centro")
        self.izquierda = izquierda + 10
        self.color = pilas.colores.blanco

        self.y = abajo + 20 - 50
        self.y = [self.y + 50]
        self.fijo = True

        #pilas.escena_actual().tareas.una_vez(retraso, self.eliminar)

    def obtener_bordes(self):
        return self.pilas.obtener_widget().obtener_bordes()