# -*- encoding: utf-8 -*-
from pilasengine import habilidades

class SeguirAlMouse(habilidades.Habilidad):
    "Hace que un actor siga la posición del mouse en todo momento."

    def iniciar(self, receptor):
        super(SeguirAlMouse, self).iniciar(receptor)
        self.pilas.eventos.mueve_mouse.conectar(self.mover)

    def mover(self, evento):
        self.receptor.x = evento.x
        self.receptor.y = evento.y