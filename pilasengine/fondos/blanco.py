# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.fondos.color import Color
from pilasengine import colores


class Blanco(Color):

    def __init__(self, pilas):
        Color.__init__(self, pilas, colores.blanco_transparente)
