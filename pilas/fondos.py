# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class Volley(pilas.actores.Actor):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        pilas.actores.Actor.__init__(self, "volley.png")
        self.z = 100

