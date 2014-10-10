# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores import Actor
from pilasengine.habilidades.puede_explotar import PuedeExplotar


class PuedeExplotarConHumo(PuedeExplotar):
    "Hace que un actor se pueda hacer explotar invocando al metodo eliminar."

    def crear_explosion(self):
        return self.pilas.actores.ExplosionDeHumo()