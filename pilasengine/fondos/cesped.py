# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.fondos import fondo_mozaico


class Cesped(fondo_mozaico.FondoMozaico):

    def iniciar(self):
        self.imagen = "fondos/cesped.png"