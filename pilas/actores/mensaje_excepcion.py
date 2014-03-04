# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import sys
import traceback

from pilas.actores import Actor
import pilas

class MensajeExcepcion(Actor):

    def __init__(self, excepcion_de_python, x=0, y=0):
        Actor.__init__(self, "invisible.png")
        mensaje_titulo = str(excepcion_de_python)
        mensaje_descripcion = str(traceback.format_exc())

        titulo = pilas.actores.Texto("ERROR: " + mensaje_titulo, y=90, ancho=500)
        descripcion = pilas.actores.Texto(mensaje_descripcion, magnitud=12, y=-50, ancho=500)

        titulo.fijo = True
        descripcion.fijo = True

        traceback.tb_lineno

        superficie = pilas.imagenes.cargar_superficie(800, 300)
        superficie.pintar(pilas.colores.negro)
        actor = pilas.actores.Actor(superficie)
        actor.transparencia = 50
        actor.z = titulo.z + 2
