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

        ## inicio: mover a otro metodo
        superficie = self.pilas.imagenes.crear_superficie(200, 200)
        #superficie.pintar(pilasengine.colores.rojo)
        #superficie.texto("Hola mundo!", 0, 0, 20)
        ## fin : mover a otro metodo


        actor = self.pilas.actores.Texto()
        self.assertTrue(actor, "Puede crear un actor texto.")
