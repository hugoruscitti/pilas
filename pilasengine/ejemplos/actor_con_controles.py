# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine
from pilasengine.actores import mono

pilas = pilasengine.iniciar()

class MonoConControles(mono.Mono):
	def actualizar(self):
		if self.pilas.escena_actual().control.arriba:
			self.y += 1
		elif self.pilas.escena_actual().control.abajo:
			self.y -= 1

		if self.pilas.escena_actual().control.izquierda:
			self.x -= 1
		elif self.pilas.escena_actual().control.derecha:
			self.x += 1

		if self.pilas.escena_actual().control.boton:
			self.saltar()

aceituna = MonoConControles(pilas)

pilas.ejecutar()