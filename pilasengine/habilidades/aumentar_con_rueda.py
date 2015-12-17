# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades


class AumentarConRueda(habilidades.Habilidad):
    
    def iniciar(self, receptor):
        super(AumentarConRueda, self).iniciar(receptor)
        self.pilas.eventos.mueve_rueda.conectar(self.cambiar_de_escala)

    def cambiar_de_escala(self, evento):
        self.receptor.escala += evento.delta/4.0
