import sys
import unittest
from PyQt4 import QtGui

import pilasengine

class TestIniciar(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testIniciaronTodosLosModulos(self):
        self.assertTrue(self.pilas.actores, "Existe el modulo actores")
        self.assertTrue(self.pilas.escenas, "Existe el modulo escenas")
        self.assertTrue(self.pilas.imagenes, "Existe el modulo escenas")
        self.assertTrue(self.pilas.utils, "Existe el modulo escenas")
        self.assertTrue(self.pilas.widget, "Existe el componente widget")

    def testPuedeCrearUnActor(self):
        un_actor = self.pilas.actores.Aceituna()
        self.assertTrue(un_actor, "Existe el actor")
        self.assertEquals(un_actor.x, 0, "Se ubica en la posicion x=0")
        self.assertEquals(un_actor.y, 0, "Se ubica en la posicion y=0")

    def testAreaDePantalla(self):
        centro = self.pilas.obtener_centro_fisico()
        self.assertEqual((320, 240), centro,
                         "El centro es la mitad de 640x480")

if __name__ == "__main__":
    unittest.main()