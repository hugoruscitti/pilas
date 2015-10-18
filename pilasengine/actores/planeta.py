# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class Planeta(Actor):
    """Representa un planeta para utilizar con el ovni.

        .. image:: ../../pilas/data/manual/imagenes/actores/planeta_azul.png

    """

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.cambiar_color('azul')

    def cambiar_color(self, color):
        if color in ['azul', 'marron', 'naranja', 'rojo', 'verde']:
            self.imagen = self.pilas.imagenes.cargar("planeta_{}.png".format(color))
        else:
            raise Exception("No se puede definir el color " + color)

    def actualizar(self):
        pass
