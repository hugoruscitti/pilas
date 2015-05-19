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

    def testFallaConHabilidadInvalida(self):

        class MiHabilidadInvalida():
            def actualizar(self):
                pass

        actor = self.pilas.actores.Aceituna()
        with self.assertRaises(Exception):
            actor.aprender(MiHabilidadInvalida)

    def testPuedeAprenderHabilidadesUsandoStrings(self):
        actor = self.pilas.actores.Aceituna()
        actor.aprender('arrastrable')
        self.assertTrue(actor.habilidades.Arrastrable.actualizar, 'Puede acceder a la nueva habilidad')
        
    def testPuedenAprenderADisparar(self):
        actor = self.pilas.actores.Aceituna(0, 0)
        actor.aprender(self.pilas.habilidades.Disparar,
                      #municion=self.municion,
                      angulo_salida_disparo=90,
                      frecuencia_de_disparo=6,
                      distancia=5,
                      escala=1)
        
        self.assertTrue(actor.disparar, "Tiene el método disparar")
        
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
        
        with self.assertRaises(NameError):
            actor.aprender('arrastrablen12')
        
        with self.assertRaises(NameError):
            actor.aprender('')


if __name__ == '__main__':
    unittest.main()