import sys
import unittest
from PyQt4 import QtGui

import pilasengine


class TestInterpolaciones(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeInterpolarPosiciones(self):
        un_actor = self.pilas.actores.Aceituna()
        un_actor.x = [100]
        un_actor.y = [100]

        self.assertEqual(0, un_actor.x, "La posicion inicial x es 0")

    def testPuedeInterpolarPosicionesDeBordes(self):
        un_actor = self.pilas.actores.Aceituna()
        un_actor.izquierda = [100]
        un_actor.izquierda = [100], 10

        self.assertEqual(0, un_actor.x, "La posicion inicial x es 0")

        un_actor.derecha = [100]
        un_actor.derecha = [100], 10

        self.assertEqual(0, un_actor.x, "La posicion inicial x es 0")

        un_actor.arriba = [100]
        un_actor.arriba = [100], 10

        self.assertEqual(0, un_actor.y, "La posicion inicial y es 0")

        un_actor.abajo = [100]
        un_actor.abajo = [100], 10

        self.assertEqual(0, un_actor.y, "La posicion inicial y es 0")

if __name__ == "__main__":
    unittest.main()
