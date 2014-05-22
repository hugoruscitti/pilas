# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.comportamientos.comportamiento import Comportamiento

class Comportamientos(object):
	"""Representa la forma de acceso y construcción de los Comportamientos.

	Esta clase representa el objeto creado por pilas que
	se puede acceder escribiendo ``pilas.comportamientos``. Desde aquí
	se puede acceder a los comportamientos pre-diseñados de y anexarlos
	a los actores para que los ejecuten.

	Por ejemplo, para 'hacer' un comportamiento:

		>>> mono = pilas.actores.Mono()
		>>> mono.hacer(pilas.comportamientos.Saltar)

	"""

	@property
	def Comportamiento(self):
		return self._referencia_comportamiento('comportamiento', 'Comportamiento')

	@property
	def Proyectil(self):
		return self._referencia_comportamiento('proyectil', 'Proyectil')

	def _referencia_comportamiento(self, modulo, clase):
		import importlib

		referencia_a_modulo = importlib.import_module('pilasengine.comportamientos.' + modulo)
		referencia_a_clase = getattr(referencia_a_modulo, clase)

		return referencia_a_clase