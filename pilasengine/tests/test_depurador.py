# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui

import pilasengine


class TestIniciar(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeDeshabilitarTodosLosModos(self):
        self.pilas.depurador.definir_modos(info=False,
                                           puntos_de_control=False,
                                           radios=False,
                                           areas=False,
                                           fisica=False,
                                           posiciones=False)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals([], modos)

    def testHabilitaLosModulosUnoAUno(self):
        self.pilas.depurador.definir_modos(info=True)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals(['ModoInformacionDeSistema'], modos,
                          "Habilita el modo info")

        self.pilas.depurador.definir_modos(puntos_de_control=True)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals(['ModoPuntosDeControl'], modos,
                          "Habilita el modo puntos de control")

        self.pilas.depurador.definir_modos(radios=True)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals(['ModoRadiosDeColision'], modos,
                          "Habilita el modo radios de colisión")

        self.pilas.depurador.definir_modos(areas=True)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals(['ModoArea'], modos,
                          "Habilita el modo areas de colisión")

        self.pilas.depurador.definir_modos(fisica=True)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals(['ModoFisica'], modos, "Habilita el modo fisico")

        self.pilas.depurador.definir_modos(posiciones=True)
        modos = self.pilas.depurador.obtener_modos_habilitados()
        self.assertEquals(['ModoPosicion'], modos, "Habilita el modo posición")

