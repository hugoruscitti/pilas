# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import sys
import traceback

from pilasengine.actores.actor import Actor


class MensajeError(Actor):

    def __init__(self, pilas, excepcion_de_python):
        Actor.__init__(self, pilas)
        self.transparencia = 100
        self.excepcion = excepcion_de_python

    def iniciar(self):
        mensaje_titulo = str(self.excepcion)
        mensaje_descripcion = str(traceback.format_exc())

        titulo = self.pilas.actores.Texto("ERROR: " + mensaje_titulo, y=90, ancho=500)
        descripcion = self.pilas.actores.Texto(mensaje_descripcion, magnitud=12, y=-50, ancho=500)

        titulo.fijo = True
        descripcion.fijo = True