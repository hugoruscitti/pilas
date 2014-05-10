# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui

import pilasengine

class TestActores(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearActores(self):
        actor = self.pilas.actores.Aceituna()
        self.assertTrue(actor, "Puede crear un actor.")

        actor = self.pilas.actores.Texto()
        self.assertTrue(actor, "Puede crear un actor texto.")

    def testFuncionanInterpolacionesSimples(self):
        actor = self.pilas.actores.Aceituna()
        self.assertEquals(0, actor.x, "Está en la posición inicial")

        actor.x = [100]

        self.assertEquals(0, actor.x, "Está en la posición inicial")
        escena = self.pilas.obtener_escena_actual()
        escena.actualizar_interpolaciones()
        self.assertTrue(actor.x > 0, "El actor se mueve un poco a la derecha")


        # Simula el paso de un segundo
        import time
        time.sleep(0.5)

        escena.actualizar_interpolaciones()
        self.assertTrue(actor.x == 100, actor.x)

if __name__ == '__main__':
    unittest.main()