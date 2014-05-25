# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine
from pilasengine.actores import mono

pilas = pilasengine.iniciar()


class MonoConControles(mono.Mono):
    def actualizar(self):
        if self.pilas.escena_actual().control.arriba:
            self.y += 2
        elif self.pilas.escena_actual().control.abajo:
            self.y -= 2

        if self.pilas.escena_actual().control.izquierda:
            self.x -= 2
        elif self.pilas.escena_actual().control.derecha:
            self.x += 2

        if self.pilas.escena_actual().control.boton:
            self.saltar()

mono_con_controles = MonoConControles(pilas)

pilas.ejecutar()