# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.habilidades.habilidad import Habilidad


class SiempreEnElCentro(Habilidad):
    """Hace que un actor siempre esté en el centro de la camara y la desplace
    cuando el actor se desplaza."""

    def actualizar(self):
        self.pilas.escena_actual().camara.x = self.receptor.x
        self.pilas.escena_actual().camara.y = self.receptor.y