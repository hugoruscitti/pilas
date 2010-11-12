# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

def comer(mono, banana):
    mono.sonreir()
    banana.eliminar()

class Colisiones(pilas.escenas.Normal):
    """Es una escena que tiene un mono y algunas frutas para comer."""


    def __init__(self):
        pilas.escenas.Normal.__init__(self, pilas.colores.gris_oscuro)
        self.crear_personajes()

        pilas.colisiones.agregar([self.mono], self.bananas, comer)
        pilas.avisar("Utilice el mouse para mover al mono y comer")

    def crear_personajes(self):
        self.mono = pilas.actores.Mono()
        self.mono.aprender(pilas.habilidades.Arrastrable)

        self.bananas = pilas.atajos.fabricar(pilas.actores.Banana, 20)
        



