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
    def __init__(self, pilas, texto="Sin texto", magnitud=20, retraso=5):
        """Inicializa el texto.

        :param texto: Texto a mostrar.
        :param magnitud: Tamaño del texto.
        """
        Texto.__init__(self, pilas, texto, magnitud)
        izquierda, _, _, abajo = self.obtener_bordes()

        self.z = -100
        TextoInferior.anterior_texto = self

        self.centro = ("centro", "centro")
        self.izquierda = izquierda + 10
        self.color = pilas.colores.blanco

        self.altura_desvanecimiento = magnitud * 2.5
        self.y = abajo + magnitud - self.altura_desvanecimiento
        self.y = [self.y + self.altura_desvanecimiento]
        self.fijo = True

        pilas.tareas.una_vez(retraso, self.desvanecer)

    def desvanecer(self):
        self.y = [self.y - self.altura_desvanecimiento]
        self.pilas.tareas.una_vez(1, self.eliminar)

    def obtener_bordes(self):
        return self.pilas.obtener_widget().obtener_bordes()