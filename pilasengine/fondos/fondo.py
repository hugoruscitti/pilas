# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.actores import actor


class Fondo(actor.Actor):
    """Representa un fondo de pantalla.

    Los fondos en pilas son actores normales, solo
    que generalmente están por detrás de toda la
    escena y ocupan toda el area de la ventana.
    """

    def __init__(self, pilas=None, imagen=None):
        super(Fondo, self).__init__(pilas)

        if imagen:
            self.imagen = imagen

        self.z = 1000
        self.radio_de_colision = None

    def pre_iniciar(self, *k, **kw):
        pass
        
    def obtener_z(self):
        return self._z

    def definir_z(self, z):
        self._z = z
        self.pilas.escena_actual()._actores.sort()

    z = property(obtener_z, definir_z,
                 doc="Define lejania respecto del observador.")
