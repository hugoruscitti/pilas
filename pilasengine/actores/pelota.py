# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class Pelota(Actor):
    """Representa una pelota de Volley, que puede rebotar e interactuar con la
    física del escenario.
    """

    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar('pelota.png')
        self.radio_de_colision = 25
        self.aprender(self.pilas.habilidades.RebotarComoPelota)