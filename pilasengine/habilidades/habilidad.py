# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


class Habilidad(object):
    """Representa una habilidad que los actores pueden aprender """
    
    def __init__(self, pilas):
        self.pilas = pilas

    def iniciar(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        pass

    def eliminar(self):
        self.receptor.eliminar_habilidad(self.__class__)

    def __repr__(self):
        return '<Habilidad: {0}>'.format(self.__class__.__name__)
