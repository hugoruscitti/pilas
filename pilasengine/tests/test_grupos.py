# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui

import pilasengine

class Test(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearGrupos(self):
        grupo = self.pilas.actores.Grupo()
        self.assertTrue(grupo, "Se pueden crear grupos")

    def testCuentaCorrectamenteActoresDentroDeGrupos(self):
        grupo = self.pilas.actores.Grupo()
        self.assertEquals(grupo.obtener_cantidad_de_actores(), 0,
                          "Hay 0 _actores al crear un grupo")

        actor = self.pilas.actores.Aceituna()
        grupo.agregar(actor)

        self.assertEquals(grupo.obtener_cantidad_de_actores(), 1,
                          "Hay 0 _actores al crear un grupo")
        self.assertEquals(grupo.obtener_actores(), [actor],
                          "Retoran correctamente los _actores")

        grupo.eliminar(actor)

        self.assertEquals(grupo.obtener_actores(), [],
                          "Borra correctamente un actor")
        self.assertEquals(grupo.obtener_cantidad_de_actores(), 0,
                          "El grupo vuelve a estar vacío")

    def testRechazaAgregarNoActores(self):
        grupo = self.pilas.actores.Grupo()

        def intentar_agregar_una_clase():
            # lo rechaza porque no es objeto, es una clase.
            grupo.agregar(self.pilas.actores.Aceituna)

        def intentar_agregar_un_objeto_cualquiera():
            grupo.agregar("hola?")

        self.assertRaises(Exception, intentar_agregar_una_clase,
                          "No debe permitir agregar clases")
        self.assertRaises(Exception, intentar_agregar_una_clase,
                          "No debe permitir agregar cosas que no sean actores")

    def testLosGruposSonBidireccionales(self):
        actor = self.pilas.actores.Aceituna()
        self.assertEqual(1, actor.obtener_cantidad_de_grupos_al_que_pertenece(),
                         "Está en un solo grupo")

        grupo = self.pilas.actores.Grupo()
        grupo.agregar(actor)
        self.assertEqual(2, actor.obtener_cantidad_de_grupos_al_que_pertenece(),
                         "Pasa a estar en dos grupos")
        grupo.eliminar(actor)
        self.assertEqual(1, actor.obtener_cantidad_de_grupos_al_que_pertenece(),
                         "Regresa a estar en un solo grupo")

if __name__ == "__main__":
    unittest.main()