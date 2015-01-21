# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores import Actor
from pilasengine.habilidades.habilidad import Habilidad


class PuedeExplotar(Habilidad):
    "Hace que un actor se pueda hacer explotar invocando al metodo eliminar."

    def iniciar(self, receptor):
        super(PuedeExplotar, self).iniciar(receptor)
        receptor.eliminar = self.eliminar_y_explotar

    def eliminar_y_explotar(self):
        explosion = self.crear_explosion()
        explosion.x = self.receptor.x
        explosion.y = self.receptor.y
        Actor.eliminar(self.receptor)
        
    def crear_explosion(self):
        a = self.pilas.actores.Explosion()
        a.escala = self.receptor.escala * 2
        return a