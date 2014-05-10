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
        self.assertTrue(self.pilas.habilidades, 'Existe el modulo habilidades')
        self.assertTrue(self.pilas.utils, "Existe el modulo escenas")
        self.assertTrue(self.pilas.widget, "Existe el componente widget")

    def testPuedeCrearUnActor(self):
        un_actor = self.pilas.actores.Aceituna()
        self.assertTrue(un_actor, "Existe el actor")
        self.assertEquals(un_actor.x, 0, "Se ubica en la posicion x=0")
        self.assertEquals(un_actor.y, 0, "Se ubica en la posicion y=0")

    def  testPuedeEliminarUnActor(self):
        actor = self.pilas.actores.Aceituna()
        self.assertTrue(actor, "Creando un actor")
        actor.eliminar()

    def testAreaDePantalla(self):
        centro = self.pilas.obtener_centro_fisico()
        self.assertEqual((320, 240), centro,
                         "El centro es la mitad de 640x480")

    def testPuedeDetenerBucle(self):
        self.pilas.widget.detener_bucle_principal()

        def intentar_detener_de_nuevo():
            self.pilas.widget.detener_bucle_principal()

        self.assertRaises(Exception, intentar_detener_de_nuevo, "No se permite detener el bucle dos veces")

        self.pilas.widget.reiniciar_bucle_principal()

        def intentar_reiniciar_de_nuevo():
            self.pilas.widget.reiniciar_bucle_principal()

        self.assertRaises(Exception, intentar_reiniciar_de_nuevo, "No se permite reiniciar al bucle dos veces")

if __name__ == "__main__":
    unittest.main()