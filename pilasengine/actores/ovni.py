# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor

class Ovni(Actor):
    """Representa Ovni que explota al momento de ser eliminado.

        .. image:: images/actores/ovni.png

    """

    def iniciar(self):
        self.imagen = "ovni.png"
        self.aprender(self.pilas.habilidades.PuedeExplotar)

    def actualizar(self):
        pass
