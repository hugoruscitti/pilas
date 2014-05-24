# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import musica


class Musica(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def cargar(self, ruta):
        ruta_al_sonido = self.pilas.obtener_ruta_al_recurso(ruta)
        return musica.Musica(ruta_al_sonido)