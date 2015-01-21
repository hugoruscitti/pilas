import sys
import unittest
from PyQt4 import QtGui

import pilasengine


class TestFondos(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearUnFondo(self):
        fondo = self.pilas.fondos.Plano()
        self.assertTrue(fondo, "Puede hacer un fondo.")
