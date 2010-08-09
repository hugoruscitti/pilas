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

def remove_an_actor(actor):
    all.remove(actor)

class Actor(sf.Sprite, object):
    """Representa un objeto visible en pantalla, algo que se ve y tiene posicion.

    Un objeto Actor se tiene que crear siempre indicando la imagen, ya
    sea como una ruta a un archivo como con un objeto Image. Por ejemplo::

        protagonista = Actor("protagonista_de_frente.png")

    es equivalente a:

        imagen = pilas.image.load("protagonista_de_frente.png")
        protagonista = Actor(imagen)

    Luego, na vez que ha sido ejecutada la sentencia aparecerá en el centro de
    la pantalla el nuevo actor para que pueda manipularlo. Por ejemplo
    alterando sus propiedades::

        protagonista.x = 100
        protagonista.scale = 2
        protagonista.rotation = 30


    Estas propiedades tambien se pueden manipular mediante
    interpolaciones. Por ejemplo, para aumentar el tamaño del
    personaje de 1 a 5 en 7 segundos::

        protagonista.scale = pilas.interpolate(1, 5, 7)
    """

    def __init__(self, image):

        if isinstance(image, str):
            image = pilas.image.load(image)

        sf.Sprite.__init__(self, image)
        insert_as_new_actor(self)
        self._set_central_axis()

        # define la posicion inicial.
        self.SetPosition(320, 240)

    def _set_central_axis(self):
        "Hace que el eje de posición del actor sea el centro de la imagen."
        size = self.GetSize()
        self.SetCenter(size[0]/2, size[1]/2)

    def get_x(self):
        x, y = self.GetPosition()
        return x

    def set_x(self, x):
        if pilas.utils.is_interpolation(x):
            self.set_x(x.from_value)
            pilas.tweener.addTween(self, set_x=x.to_value, tweenTime=x.duration * 1000)
        else:
            self.SetX(x)

    def set_y(self, y):
        if pilas.utils.is_interpolation(y):
            self.set_y(y.from_value)
            pilas.tweener.addTween(self, set_y=y.to_value, tweenTime=y.duration * 1000)
        else:
            self.SetY(y)

    def get_y(self):
        x, y = self.GetPosition()
        return y

    def set_scale(self, s):
        if pilas.utils.is_interpolation(s):
            self.set_scale(s.from_value)
            pilas.tweener.addTween(self, set_scale=s.to_value, tweenTime=s.duration * 1000)
        else:
            self.SetScale(s, s)

    def get_scale(self):
        # se asume que la escala del personaje es la horizontal.
        return self.GetScale()[0]

    def get_rotation(self):
        return -self.GetRotation()

    def set_rotation(self, x):

        if pilas.utils.is_interpolation(x):
            self.set_rotation(x.from_value)
            pilas.tweener.addTween(self, set_rotation=x.to_value, tweenTime=x.duration * 1000)
        else:
            self.SetRotation(-x)

    x = property(get_x, set_x, doc="Define la posición horizontal.")
    y = property(get_y, set_y, doc="Define la posición vertical.")
    rotation = property(get_rotation, set_rotation, doc="Angulo de rotación (en grados, de 0 a 360)")
    scale = property(get_scale, set_scale, doc="Escala de tamaño, 1 es normal, 2 al doble de tamaño etc...)")

    def kill(self):
        "Elimina el actor de la lista de actores que se imprimen en pantalla."
        remove_an_actor(self)

    def update(self):
        "Actualiza el estado del actor. Este metodo se llama una vez por frame."
        pass


class Monkey(Actor):
    """Representa la cara de un mono de color marrón.

    Este personaje se usa como ejemplo básico de un actor. Sus
    métodos mas usados son:

    - smile
    - shout

    El primero hace que el mono se ría y el segundo que grite.
    """

    def __init__(self):
        # carga las imagenes adicionales.
        self.image_normal = pilas.image.load('monkey_normal.png')
        self.image_smile = pilas.image.load('monkey_smile.png')
        self.image_shout = pilas.image.load('monkey_shout.png')

        # Inicializa el actor.
        Actor.__init__(self, self.image_normal)

    def smile(self):
        self.SetImage(self.image_smile)
        # Luego de un segundo regresa a la normalidad
        pilas.add_task(1, self.normal)

    def shout(self):
        self.SetImage(self.image_shout)
        # Luego de un segundo regresa a la normalidad
        pilas.add_task(1, self.normal)

    def normal(self):
        self.SetImage(self.image_normal)
