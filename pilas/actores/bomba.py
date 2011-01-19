# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion
from pilas.actores import Explosion

class Bomba(Animacion):
    """Representa una explosion para una bomba, dinamita etc...

    La bomba adquiere la habilidad explotar al momento de crearse, así
    que puedes invocar a su método "explotar" y la bomba hará un
    explosión con sonido en pantalla.

    Este es un ejemplo de uso del actor::

        bomba = pilas.actores.Bomba()
        bomba.explotar()
    """


    def __init__(self, x=0, y=0):
        Animacion.__init__(self, pilas.imagenes.Grilla("bomba.png", 2), ciclica=True, x=x, y=y)
        self.radio_de_colision = 25
        self.aprender(pilas.habilidades.PuedeExplotar)

    def explotar(self):
        # Este metodo solo exite para compativilidad hacia atras.
        self.eliminar()
