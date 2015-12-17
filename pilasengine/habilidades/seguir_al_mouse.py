# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades


class SeguirAlMouse(habilidades.Habilidad):
    "Hace que un actor siga la posición del mouse en todo momento."

    def iniciar(self, receptor):
        super(SeguirAlMouse, self).iniciar(receptor)
        self.pilas.eventos.mueve_mouse.conectar(self.mover)

    def mover(self, evento):
        self.receptor.x = evento.x
        self.receptor.y = evento.y