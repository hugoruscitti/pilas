# -*- encoding: utf-8 -*-

class Habilidades(object):
	"""Representa la forma de acceso y construcción de las habilidades.

	Esta clase representa el objeto creado por pilas que
	se puede acceder escribiendo ``pilas.habilidades``. Desde aquí
	se puede acceder a las habilidades pre-diseñadas de pilas y
	'enseñarselas' a los actores.

	Por ejemplo, para 'enseñar' una habilidad:

		>>> nave = pilas.actores.Nave()
		>>> nave.aprender(pilas.habilidades.Arrastrable)

	"""

	def __init__(self, pilas):
		self.pilas = pilas

   	def Habilidad(self):
   		return self._crear_habilidad('habilidad', 'Habilidad')

	def SiempreEnElCentro(self):
		return self._crear_habilidad('siempre_en_el_centro', 'SiempreEnElCentro')

	def _crear_habilidad(self, modulo, clase):
		import importlib

		referencia_a_modulo = importlib.import_module('pilasengine.habilidades.' + modulo)
		referencia_a_clase = getattr(referencia_a_modulo, clase)

		nueva_habilidad = referencia_a_clase(self.pilas)
		return nueva_habilidad


class ProxyHabilidades(object):
	"""Implementa un intermediario con todas las habilidades del Actor."""

	def __init__(self, habilidades):
		self.habilidades = habilidades

	def __getattr__(self, name):
		su_habilidad = None

		for habilidad in self.habilidades:
			if habilidad.__class__.__name__ == name:
				su_habilidad = habilidad
				break

		if not su_habilidad:
			raise Exception("El actor no tiene asignada la habilidad " + name +
							".\n No puede acceder mediante actor.habilidades." + name)

		return su_habilidad

	def __repr__(self):
		return '<Éste actor tiene {0} habilidades: {1}>'.format(str(len(self.habilidades)), 
			str(self.habilidades))	