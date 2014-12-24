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
        habilidad = self.pilas.habilidades.Habilidad(self.pilas)
        self.assertTrue(habilidad, 'Puede crear habilidad')

    def testNoPuedeRepetirHabilidad(self):
        actor = self.pilas.actores.Aceituna()
        actor.aprender(self.pilas.habilidades.Habilidad)
        actor.aprender(self.pilas.habilidades.Habilidad)
        self.assertEquals(len(actor._habilidades), 1,
                          'No puede Repetir la habilidad')

    def testPuedeIniciarHabilidad(self):
        actor = self.pilas.actores.Aceituna()
        actor.aprender(self.pilas.habilidades.Habilidad)
        self.assertTrue(actor.habilidades.Habilidad.iniciar,
                        'Puede iniciar habilidad')

    def testPuedeActualizarHabilidad(self):
        actor = self.pilas.actores.Aceituna()
        actor.aprender(self.pilas.habilidades.Habilidad)
        self.assertTrue(actor.habilidades.Habilidad.actualizar,
                        'Puede actualizar habilidad')

    def testPuedeEliminarHabilidad(self):
        actor = self.pilas.actores.Aceituna()
        actor.aprender(self.pilas.habilidades.Habilidad)
        actor.habilidades.Habilidad.eliminar()
        self.assertEquals(actor._habilidades, list(), 'Puede eliminar habilidad')

    def testPuedeCrearHabilidadPersonalizada(self):
        class MiHabilidad(pilasengine.habilidades.Habilidad):
                def actualizar(self):
                    pass

        actor = self.pilas.actores.Aceituna()
        actor.aprender(MiHabilidad)

        self.assertEquals(1, len(actor._habilidades),
                          'Pude aprender habilidad personalizada')

        def crear_habilidad_incorrectamente():
            class MiHabilidad():
                def actualizar(self):
                    pass

            actor = self.pilas.actores.Aceituna()
            actor.aprender(MiHabilidad)
        self.assertRaises(Exception, crear_habilidad_incorrectamente)

    def testPuedeAprenderHabilidadesUsandoStrings(self):
        actor = self.pilas.actores.Aceituna()
        actor.aprender('arrastrable')
        self.assertTrue(actor.habilidades.Arrastrable.actualizar, 'Puede acceder a la nueva habilidad')
        
    def testPuedeAprenderHabilidadPersonalizadaUsandoStrings(self):
        class MiHabilidad(pilasengine.habilidades.Habilidad):
            def actualizar(self):
                pass

        actor = self.pilas.actores.Aceituna()
        
        self.pilas.habilidades.vincular(MiHabilidad)
        
        actor.aprender('mihabilidad')

        self.assertEquals(1, len(actor._habilidades), 'Pude aprender habilidad personalizada desde string')
        
    def testPuedeReportarErroresAlAprenderHabilidadesIncorrectamente(self):
        actor = self.pilas.actores.Aceituna()
        
        def asociar_habilidad_incorrectamente_1():
            actor.aprender('arrastrablen12')
        
        def asociar_habilidad_incorrectamente_2():
            actor.aprender('')
        
        self.assertRaises(NameError, asociar_habilidad_incorrectamente_1)
        self.assertRaises(NameError, asociar_habilidad_incorrectamente_2)


if __name__ == '__main__':
    unittest.main()