# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import colores

class Interfaz(object):
    """Representa la propiedad pilas.fondos

    Este objeto se encarga de hacer accesible
    la creación de fondos para las escenas.
    """

    def __init__(self, pilas):
        self.pilas = pilas

    def Boton(self, texto='Sin texto'):
        import boton
        return boton.Boton(self.pilas, texto)

    def Deslizador(self):
        import deslizador
        return deslizador.Deslizador(self.pilas)