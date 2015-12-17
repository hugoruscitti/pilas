# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades


class SeguirClicks(habilidades.Habilidad):

    def iniciar(self, receptor):
        super(SeguirClicks, self).iniciar(receptor)
        self.pilas.eventos.click_de_mouse.conectar(self.moverse_a_este_punto)

    def moverse_a_este_punto(self, evento):
        self.receptor.x = [evento.x], 0.5
        self.receptor.y = [evento.y], 0.5
