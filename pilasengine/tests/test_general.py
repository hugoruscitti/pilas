# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui
import pilasengine


class TestGeneral(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        import pilasengine
        self.pilas = pilasengine.iniciar()

    def testEscribirConAvisar(self):
        actor = self.pilas.avisar("Hola mundo !!")

if __name__ == '__main__':
    unittest.main()