# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


class Comportamiento(object):
    "Representa un comportamiento (estrategia) que se puede anexar a un actor."

    def __init__(self, pilas=None):
        self.pilas = pilas

    def iniciar(self, receptor):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        if getattr(self, 'pilas', None) is None:
            self.pilas = receptor.pilas

        self.receptor = receptor

    def actualizar(self):
        """Actualiza el comportamiento en un instante dado.

        Si este metodo retorna True entonces el actor dejará
        de ejecutar este comportamiento."""
        pass

    def terminar(self):
        pass
