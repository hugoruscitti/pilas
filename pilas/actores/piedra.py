# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class Piedra(Actor):
    "Representa un bloque que tiene fisica como una caja."

    def __init__(self, x=0, y=0, tamano="grande", dx=0, dy=0):
        imagen = pilas.imagenes.cargar('piedra_' + tamano + '.png')
        Actor.__init__(self, imagen)
        self.rotacion = 0
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        radios = {
                'grande': 25,
                'media': 20,
                'chica': 10,
                }

        self.radio_de_colision = radios[tamano]

    def actualizar(self):
        self.rotacion += 1
        self.x += self.dx
        self.y += self.dy

        self._reincorporarse_si_sale_del_escenario()

    def _reincorporarse_si_sale_del_escenario(self):
        """Se asegura de que la piedra regrese a la pantalla si sale.

        Si la piedra sale por la derecha de la pantalla, entonces regresa
        por la izquiera. Si sale por arriba regresa por abajo y asi..."""

        # Se asegura de regresar por izquierda y derecha.
        if self.derecha < -320:
            self.izquierda = 320
        elif self.izquierda > 320:
            self.derecha = -320

        # Se asegura de regresar por arriba y abajo.
        if self.abajo > 240:
            self.arriba = -240
        elif self.arriba < -240:
            self.abajo = 240

