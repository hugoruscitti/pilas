# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas
from PySFML import sf

class Escena(Actor):
    "Escena abstracta."

    def __init__(self):
        pilas.definir_escena(self)

    def actualizar(self):
        pass


class Paisaje(Escena):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Escena.__init__(self)
        Actor.__init__(self, "volley.png")
        self.z = 100

class Normal(Escena):
    "Representa la escena inicial mas simple."

    def __init__(self, color_de_fondo=None):
        Escena.__init__(self)
        self.fondo = color_de_fondo or sf.Color(200, 200, 200)

    def dibujar(self, aplicacion):
        aplicacion.Clear(self.fondo)
