# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from .texto import Texto


class TextoInferior(Texto):
    """Representa un texto al pie de la ventana.

    Esta clase se utiliza desde el método "pilas.avisar()".
    """
    anterior_texto = None

    def __init__(self, texto="None", x=0, y=0, magnitud=17, autoeliminar=False, retraso=5):
        """Inicializa el texto.

        :param texto: Texto a mostrar.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param magnitud: Tamaño del texto.
        :param vertical: Si el texto será vertical u horizontal, como True o False.
        """
        Texto.__init__(self, texto, x, y, magnitud)
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        # Se asegura de que solo exista un texto inferior
        if TextoInferior.anterior_texto:
            TextoInferior.anterior_texto.eliminar()

        self.z = -100
        TextoInferior.anterior_texto = self

        self.centro = ("centro", "centro")
        self.izquierda = izquierda + 10
        self.color = pilas.colores.blanco
        self.abajo = abajo + 10
        self.fijo = True

        self._crear_sombra()

        if autoeliminar:
            pilas.escena_actual().tareas.una_vez(retraso, self.eliminar)

    def _crear_sombra(self):
        """Genera una sombra para el texto."""
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        imagen = pilas.imagenes.cargar_superficie(derecha - izquierda, self.alto + 15)
        imagen.pintar(pilas.colores.negro_transparente)

        self.sombra = pilas.actores.Actor(imagen)
        self.sombra.z = self.z + 1
        self.sombra.fijo = True
        self.sombra.abajo = self.abajo - 10
        self.sombra.izquierda = izquierda

    def eliminar(self):
        """Quita el texto de la escena."""
        Texto.eliminar(self)
        self.sombra.eliminar()
