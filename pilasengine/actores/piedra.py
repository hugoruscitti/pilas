# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class Piedra(Actor):
    """Representa una piedra que podría ser usada como meteoríto."""

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.definir_tamano('grande')
        self.velocidad_rotacion = 1
        self.dx = 0
        self.dy = 0

    def definir_tamano(self, tamano):
        if tamano not in ['grande', 'media', 'chica']:
            raise Exception("El tamano indicado es incorrecto, solo se permite \
                            grande', 'media' o 'chica'.")

        self.imagen = self.pilas.imagenes.cargar('piedra_' + tamano + '.png')
        radios = {'grande': 25, 'media': 20, 'chica': 10}

        self.radio_de_colision = radios[tamano]
        self.aprender(self.pilas.habilidades.SeMantieneEnPantalla)

    def actualizar(self):
        "Realiza una actualización de la posición."
        self.rotacion += self.velocidad_rotacion
        self.x += self.dx
        self.y += self.dy

    def empujar(self, dx, dy):
        self.dx = dx
        self.dy = dy