# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.animacion import Animacion

class ExplosionDeHumo(Animacion):
    """Representa una explosion para una bomba, dinamita etc...

    Este actor se puede anexar a cualquier a otro
    para producir un efecto de explosión, por ejemplo::

        >>> actor = pilas.actores.Aceituna()
        >>> actor.aprender(pilas.habilidades.PuedeExplotarConHumo)
        >>> actor.eliminar()
    """

    def __init__(self, pilas, x, y):
        grilla = pilas.imagenes.cargar_grilla("efecto_humo_1.png", 10)
        Animacion.__init__(self, pilas, grilla, ciclica=False, x=x, y=y,
                           velocidad=15)
