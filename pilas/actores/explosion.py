# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion

class Explosion(Animacion):
    """Representa una explosion para una bomba, dinamita etc...

    El actor simplemente aparece reproduciendo un sonido y
    haciendo una animación:

        >>> actor = pilas.actores.Bomba()

    .. image:: images/actores/explosion.png

    y una vez que termina se elimina a sí mismo.

    Este actor también se puede anexar a cualquier
    otro para producir explosiones. Cuando enseñamos a un
    actor a explotar (por ejemplo un pingüino), el actor 
    ``Explosion`` aparece cuando se elimina al actor::

        >>> actor = pilas.actores.Pingu()
        >>> actor.aprender(pilas.habilidades.PuedeExplotar)
        >>> actor.eliminar()
    """


    def __init__(self, x=0, y=0):
        grilla = pilas.imagenes.cargar_grilla("explosion.png", 7)
        Animacion.__init__(self, grilla, x=x, y=y)
        self.sonido_explosion = pilas.sonidos.cargar("explosion.wav")
        self.sonido_explosion.reproducir()
