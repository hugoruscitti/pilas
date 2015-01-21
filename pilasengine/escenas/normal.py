# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.escenas.escena import Escena


class Normal(Escena):

    def iniciar(self):
        self.fondo = self.pilas.fondos.Plano()

    def actualizar(self):
        pass

    def terminar(self):
        pass