# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import random

from pilasengine import habilidades


class RebotarComoCaja(habilidades.Habilidad):
    """Le indica al actor que rebote y colisiones como una caja cuadrada.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.RebotarComoPelota)
    """

    def iniciar(self, receptor):
        super(RebotarComoCaja, self).iniciar(receptor)
        error = random.randint(-10, 10) / 10.0
        rectangulo = self.pilas.fisica.Rectangulo(receptor.x + error,
                                                  receptor.y + error,
                                                  receptor.radio_de_colision *
                                                  2 - 4,
                                                  receptor.radio_de_colision *
                                                  2 - 4,)
        receptor.aprender(self.pilas.habilidades.Imitar, rectangulo)

    def eliminar(self):
        super(RebotarComoCaja, self).eliminar()
        self.receptor.habilidades.Imitar.eliminar()
