# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import random

from pilasengine import habilidades


class RebotarComoPelota(habilidades.Habilidad):
    """Le indica al actor que rebote y colisiones como una pelota.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.RebotarComoPelota)
    """

    def iniciar(self, receptor):
        super(RebotarComoPelota, self).iniciar(receptor)
        error = random.randint(-10, 10) / 10.0

        circulo = self.pilas.fisica.Circulo(receptor.x + error,
                                            receptor.y + error,
                                            receptor.radio_de_colision)
        receptor.aprender(self.pilas.habilidades.Imitar, circulo)
        self.circulo = circulo
        receptor.impulsar = self.impulsar
        receptor.empujar = self.empujar

    def eliminar(self):
        super(RebotarComoPelota, self).eliminar()
        self.receptor.habilidades.Imitar.eliminar()

    def impulsar(self, dx, dy):
        self.circulo.impulsar(dx, dy)

    def empujar(self, dx, dy):
        self.circulo.empujar(dx, dy)