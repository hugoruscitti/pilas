# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor

class Particula(Actor):

    def __init__(self, pilas, emisor, x, y, dx, dy, imagen, vida):
        Actor.__init__(self, pilas, x, y)
        self.emisor = emisor
        self.imagen = imagen
        self.dx = dx
        self.dy = dy

        self.vida = vida * 1000 # expresada en segundos
        self.contador = 0

        self.escala_fin = self.escala
        self.transparencia_fin = self.transparencia
        self.rotacion_fin = self.rotacion
        self.aceleracion_x = 0
        self.aceleracion_y = 0
        self.figura_de_colision = None

        if self.emisor:
            self.z = self.emisor.z

    def definir_escala_fin(self, valor):
        self._incremento_escala = (valor - self.escala) / ((self.vida / 1000.0) * 60.0)

    escala_fin = property(None, definir_escala_fin)

    def definir_transparencia_fin(self, valor):
        self._incremento_transparencia = (valor - self.transparencia) / ((self.vida / 1000.0) * 60.0)

    transparencia_fin = property(None, definir_transparencia_fin)

    def definir_rotacion_fin(self, valor):
        self._incremento_rotacion = (valor - self.rotacion) / ((self.vida / 1000.0) * 60.0)

    rotacion_fin = property(None, definir_rotacion_fin)

    def definir_aceleracion_x(self, valor):
        self._incremento_aceleracion_x = valor / ((self.vida / 1000.0) * 60.0)

    aceleracion_x = property(None, definir_aceleracion_x)

    def definir_aceleracion_y(self, valor):
        self._incremento_aceleracion_y = valor / ((self.vida / 1000.0) * 60.0)

    aceleracion_y = property(None, definir_aceleracion_y)

    def actualizar(self):
        self.contador += 16   # llega a 1000 en un segundo

        self.dx += self._incremento_aceleracion_x
        self.dy += self._incremento_aceleracion_y

        self.x += self.dx
        self.y += self.dy

        self.escala += self._incremento_escala
        self.transparencia += self._incremento_transparencia
        self.rotacion += self._incremento_rotacion

        if self.contador > self.vida:
            # Solo si tiene emisor le avisa que se eliminó.
            if self.emisor:
                self.emisor.se_elimina_particula(self)
            self.eliminar()
