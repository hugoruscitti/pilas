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

    def __init__(self, pilas, titulo, descripcion):
        self.titulo_error = titulo
        self.descripcion_error = descripcion
        Actor.__init__(self, pilas)
        self.transparencia = 100

    def iniciar(self):
        mensaje_titulo = self.titulo_error
        mensaje_descripcion = self.descripcion_error

        titulo = self.pilas.actores.Texto("ERROR: " + mensaje_titulo,
                                          y=150, ancho=500)
        descripcion = self.pilas.actores.Texto(mensaje_descripcion, magnitud=16,
                                               y=-80, ancho=500)

        titulo.fijo = True
        descripcion.fijo = True