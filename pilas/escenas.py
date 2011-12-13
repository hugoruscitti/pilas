# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class Escena(object):
    "Escena abstracta."

    def __init__(self):
        pilas.mundo.definir_escena(self)

    def iniciar(self):
        pass

    def terminar(self):
        pass


class Normal(Escena):
    "Representa la escena inicial mas simple."

    def __init__(self, color_de_fondo=None):
        Escena.__init__(self)
        self.fondo = pilas.fondos.Color(color_de_fondo)
