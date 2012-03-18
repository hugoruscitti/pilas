# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from actor import Texto

class TextoInferior(Texto):
    """Representa un texto al pie de la ventana.

    Esta clase se utiliza desde el método "pilas.avisar()".
    """
    anterior_texto = None

    def __init__(self, texto="None", x=0, y=0, magnitud=17):
        Texto.__init__(self, texto, x, y, magnitud)
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        # Se asegura de que solo exista un texto inferior
        if TextoInferior.anterior_texto:
            TextoInferior.anterior_texto.eliminar()

        TextoInferior.anterior_texto = self

        self.centro = ("centro", "centro")
        self.izquierda = izquierda + 10
        self.color = colores.blanco
        self.abajo = abajo + 10
