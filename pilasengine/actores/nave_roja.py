# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class NaveRoja(Actor):

    def iniciar(self):
        self.ruta_imagen_normal = "nave_roja/nave.png"
        self.ruta_imagen_izquierda = "nave_roja/nave_izquierda.png"
        self.ruta_imagen_derecha = "nave_roja/nave_derecha.png"

        self.radio_de_colision = 33
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.velocidad = 5

    def actualizar(self):
        control = self.pilas.control

        self.x += self.velocidad_x
        self.y += self.velocidad_y

        if control.izquierda:
            self.velocidad_x -= self.velocidad
            self.imagen = self.ruta_imagen_izquierda
        elif control.derecha:
            self.velocidad_x += self.velocidad
            self.imagen = self.ruta_imagen_derecha
        else:
            self.imagen = self.ruta_imagen_normal

        if control.arriba:
            self.velocidad_y += self.velocidad
        elif control.abajo:
            self.velocidad_y -= self.velocidad

        # Aplica una desaceleración al movimiento de la nave.
        self.velocidad_x *= 0.5
        self.velocidad_y *= 0.5

    def terminar(self):
        pass