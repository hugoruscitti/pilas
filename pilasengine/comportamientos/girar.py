# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import comportamientos


class Girar(comportamientos.Comportamiento):

    def iniciar(self, receptor, delta=360, velocidad=5):
        super(Girar, self).iniciar(receptor)

        self.grados_a_rotar = abs(self.receptor.rotacion - delta)
        if delta < 0:
            self.velocidad = -velocidad
        elif delta > 0:
            self.velocidad = velocidad
        else:
            # El actor no gira si el angulo es de 0°
            self.grados_a_rotar = 0

    def actualizar(self):
        if self.grados_a_rotar <= 0:
            return True

        self.receptor.rotacion += self.velocidad
        self.grados_a_rotar -= abs(self.velocidad)