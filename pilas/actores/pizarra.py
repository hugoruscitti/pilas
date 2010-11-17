# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import cairo

import pilas
from pilas.actores import Actor

class Lapiz:

    def __init__(self):
        self.x = 0
        self.y = 0

class Pizarra(Actor):
    """Representa una superficie de dibujo inicialmente transparente.

    Puedes pintar sobre esta pizarra usando métodos que simulan
    un lapiz, que se puede mover sobre una superficie.
    """


    def __init__(self, x=0, y=0):
        Actor.__init__(self, x=x, y=y)
        self.canvas = pilas.motor.Canvas()
        self.lapiz = Lapiz()
        self.actualizar_imagen()
        self.levantar_lapiz()
        self.mover_lapiz(0, 0)
        self.definir_centro(320, 240)

    def levantar_lapiz(self):
        self.lapiz_bajo = False

    def bajar_lapiz(self):
        self.lapiz_bajo = True

    def actualizar_imagen(self):
        "Se encarga de actualizar la vista de la pizarra."
        self.canvas.actualizar()
        self.definir_imagen(self.canvas.image)

    def pintar_punto(self, x, y):
        y = 240 - y
        x += 320
        self.canvas.context.arc(x, y, 10, 0, 2*3.1415)
        self.canvas.context.fill()
        self.actualizar_imagen()

    def mover_lapiz(self, x, y):
        if self.lapiz_bajo:
            self.canvas.context.move_to(self.lapiz.x, self.lapiz.y)
            self.canvas.context.set_line_width(3)
            self.canvas.context.line_to(x, y)
            self.canvas.context.stroke()

            # Actualiza la imagen si ha dibujado.
            self.actualizar_imagen()

        self.lapiz.x, self.lapiz.y = x, y
        
    def definir_color(self, color):
        r, g, b = color.obtener_componentes()
        self.canvas.context.set_source_rgb(r, g, b)
