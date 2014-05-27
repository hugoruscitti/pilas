# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine


class MiActor(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "spinner.png"

    def actualizar(self):
        self.rotacion += 2

pilas = pilasengine.iniciar()

pilas.actores.vincular(MiActor)
mi_actor = pilas.actores.MiActor()

#
# Otra opcion de creación
#
#   >>> MiActor(pilas)
#
# y si escribimos simplemente MiActor() se informa un error.
#

pilas.ejecutar()