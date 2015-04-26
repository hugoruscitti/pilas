# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine


class MiHabilidad(pilasengine.habilidades.Habilidad):

    def actualizar(self):
        self.receptor.rotacion += 2


pilas = pilasengine.iniciar()

aceituna = pilas.actores.Aceituna()
pilas.habilidades.vincular(MiHabilidad)
aceituna.aprender('MiHabilidad')

pilas.ejecutar()
