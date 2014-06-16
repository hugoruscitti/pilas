# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.animacion import Animacion


class Bomba(Animacion):
    """Representa una bomba que puede explotar...

    .. image:: images/actores/bomba.png

    La bomba adquiere la habilidad explotar al momento de crearse, así
    que puedes invocar a su método "explotar" y la bomba hará un
    explosión en pantalla con sonido.

    Este es un ejemplo de uso del actor:

        >>> bomba = pilas.actores.Bomba()
        >>> bomba.explotar()
    """

    def __init__(self, pilas=None, x=0, y=0):
        grilla = pilas.imagenes.cargar_grilla("bomba.png", 2)
        Animacion.__init__(self, pilas, grilla, ciclica=True, x=x, y=y,
                           velocidad=10)
        self.radio_de_colision = 25
        self.aprender(pilas.habilidades.PuedeExplotar)

    def explotar(self):
        """Hace explotar a la bomba y la elimina de la pantalla."""
        self.eliminar()
