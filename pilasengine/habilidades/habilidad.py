# -*- encoding: utf-8 -*-

class Habilidad(object):
	"""Representa una habilidad que los actores pueden aprender """
	def __init__(self, pilas):
		self.pilas = pilas

	def iniciar(self, receptor):
		self.receptor = receptor

	def actualizar(self):
		pass

	def eliminar(self):
		self.receptor.eliminar_habilidad(self.__class__)

	def __repr__(self):
		return '<Habilidad: {0}>'.format(self.__class__.__name__)