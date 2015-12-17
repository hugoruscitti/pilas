# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import musica
from pilasengine import configuracion


class Musica(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def cargar(self, ruta):
        ruta_a_la_musica = self.pilas.obtener_ruta_al_recurso(ruta)

        if self.pilas.configuracion.audio_habilitado():
            return musica.Musica(ruta_a_la_musica)
        else:
            return musica.MusicaDeshabilitada(ruta_a_la_musica)

    def habilitar(self):
        musica.Musica.deshabilitado = False
        
    def deshabilitar(self):
        musica.Musica.deshabilitado = True