# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui

import pilasengine

class TestHabilidades(unittest.TestCase):
	app = QtGui.QApplication(sys.argv)

	def setUp(self):
		self.pilas = pilasengine.iniciar()

	def testPuedeCrearHabilidad(self):
		habilidad = self.pilas.habilidades.Habilidad()
		self.assertTrue(habilidad, 'Puede crear habilidad')

	def testNoPuedeRepetirHabilidad(self):
		actor = self.pilas.actores.Aceituna()
		actor.aprender(self.pilas.habilidades.Habilidad)
		actor.aprender(self.pilas.habilidades.Habilidad)
		self.assertEquals(len(actor._habilidades), 1, 'No puede Repetir la habilidad')
	
	def testPuedeIniciarHabilidad(self):
		actor = self.pilas.actores.Aceituna()
		actor.aprender(self.pilas.habilidades.Habilidad)
		self.assertTrue(actor.habilidades.Habilidad.iniciar, 'Puede iniciar habilidad')	

	def testPuedeActualizarHabilidad(self):
		actor = self.pilas.actores.Aceituna()
		actor.aprender(self.pilas.habilidades.Habilidad)
		self.assertTrue(actor.habilidades.Habilidad.actualizar, 'Puede actualizar habilidad')	

	def testPuedeEliminarHabilidad(self):
		actor = self.pilas.actores.Aceituna()
		actor.aprender(self.pilas.habilidades.Habilidad)
		actor.habilidades.Habilidad.eliminar()
		self.assertEquals(actor._habilidades, list(), 'Puede eliminar habilidad')

if __name__ == '__main__':
	unittest.main()		