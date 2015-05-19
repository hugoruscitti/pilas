# -*- encoding: utf-8 -*-
import sys
import unittest

from PyQt4 import QtGui

import pilasengine


class TestEscenas(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearVincularUnaEscena(self):
        class EscenaNueva(pilasengine.escenas.Escena):
            pass
            
        self.pilas.escenas.vincular(EscenaNueva)
        escena = self.pilas.escenas.EscenaNueva()

        self.assertTrue(escena, "A creado la escena correctamente.")
        self.assertEqual(escena, self.pilas.escena_actual(), "Ha vinculado la escena correctamente.")
        
    def testInformaConUnaExcepcionSiFaltaArgumentoPilas(self):
        class EscenaNueva(pilasengine.escenas.Escena):
            pass

        with self.assertRaises(Exception):
            EscenaNueva()


if __name__ == '__main__':
    unittest.main()
