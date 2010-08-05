# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

from PySFML import sf

all = []

def insert_as_new_actor(actor):
    "Coloca a un actor en la lista de actores a imprimir en pantalla."
    all.append(actor)


class Actor(sf.Sprite, object):
    """Representa un objeto visible en pantalla, algo que se ve y tiene posicion.

    Un objeto Actor se tiene que crear siempre indicando la imagen
    que tiene que representar. Por ejemplo::

        protagonista = Actor("protagonista_de_frente.png")

    y una vez que ha sido creado aparecerá en el centro de la pantalla para
    que pueda manipularlo:

        protagonista.x = 100
        protagonista.scale = 2
        protagonista.rotation = 30
    """


    def __init__(self, image_path):
        image = pilas.image.load(image_path)

        sf.Sprite.__init__(self, image)
        insert_as_new_actor(self)
        self._set_central_axis()

        # define la posicion inicial.
        self.SetPosition(320, 240)

    def _set_central_axis(self):
        "Hace que el eje de posición del actor sea el centro de la imagen."
        size = self.GetSize()
        self.SetCenter(size[0]/2, size[1]/2)

    def GetX(self):
        x, y = self.GetPosition()
        return x

    def GetY(self):
        x, y = self.GetPosition()
        return y

    x = property(GetX, sf.Sprite.SetX)
    y = property(GetY, sf.Sprite.SetY)
    rotation = property(sf.Sprite.GetRotation, sf.Sprite.SetRotation)


class Monkey(Actor):

    def __init__(self):
        Actor.__init__(self, 'monkey_normal.png')
