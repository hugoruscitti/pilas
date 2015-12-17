# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.animacion import Animacion

class Explosion(Animacion):
    """Representa una explosion para una bomba, dinamita etc...

    El actor simplemente aparece reproduciendo un sonido y
    haciendo una animación:

        >>> actor = pilas.actores.Bomba()

    .. image:: ../../pilas/data/manual/imagenes/actores/explosion.png

    y una vez que termina se elimina a sí mismo.

    Este actor también se puede anexar a cualquier
    otro para producir explosiones. Cuando enseñamos a un
    actor a explotar (por ejemplo un pingüino), el actor
    ``Explosion`` aparece cuando se elimina al actor::

        >>> actor = pilas.actores.Pingu()
        >>> actor.aprender(pilas.habilidades.PuedeExplotar)
        >>> actor.eliminar()
    """

    def __init__(self, pilas, x, y):
        grilla = pilas.imagenes.cargar_grilla("explosion.png", 7)
        Animacion.__init__(self, pilas, grilla, ciclica=False, x=x, y=y,
                           velocidad=10)
        self.sonido_explosion = pilas.sonidos.cargar("audio/explosion.wav")
        self.sonido_explosion.reproducir()
