# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Ejes(Actor):
    """Representa el eje de coordenadas tomado como sistema de referencia.

    Este actor es útil para mostrar que la ventana
    de pilas tiene una referencia, y que las posiciones
    responden a este modelo.

    Para crear el eje podrías ejecutar:

        >>> eje = pilas.actore.Eje()

    """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = "ejes.png"
        self.z = 999

    def actualizar(self):
        pass

    def terminar(self):
        pass
