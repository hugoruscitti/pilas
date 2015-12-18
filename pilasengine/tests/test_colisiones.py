# -*- encoding: utf-8 -*-
import sys
import time
import unittest

from PyQt4 import QtGui

import pilasengine


class TestColisiones(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar(modo_test=True)

    def testColisionesEntreActores(self):
        mono = self.pilas.actores.Mono()
        aceituna = self.pilas.actores.Aceituna()

        def colisionan(actor1, actor2):
            self.assertEquals(actor1.id, mono.id)
            self.assertEquals(actor2.id, aceituna.id)

        self.pilas.colisiones.agregar(mono, aceituna, colisionan)
        self.pilas.colisiones.notificar_colision(mono.figura_de_colision, aceituna.figura_de_colision)

        # Dispara las funciones de colision.
        self.pilas.colisiones.actualizar()

    def testColisionesEntreEtiquetasDeActores(self):
        mono = self.pilas.actores.Mono()
        aceituna = self.pilas.actores.Aceituna()

        def colisionan(actor1, actor2):
            self.assertEquals(actor1.id, mono.id)
            self.assertEquals(actor2.id, aceituna.id)

        self.pilas.colisiones.agregar("mono", "aceituna", colisionan)
        self.pilas.colisiones.notificar_colision(mono.figura_de_colision, aceituna.figura_de_colision)

        # Dispara las funciones de colision.
        self.pilas.colisiones.actualizar()

    def testColisionesEntreFiguras(self):
        circulo = self.pilas.fisica.Circulo()
        rectangulo = self.pilas.fisica.Rectangulo(0, 0, 100, 100)

        def colisionan(figura1, figura2):
            self.assertEquals(figura1.id, circulo.id)
            self.assertEquals(figura2.id, rectangulo.id)

        self.pilas.colisiones.agregar(circulo, rectangulo, colisionan)
        self.pilas.colisiones.notificar_colision(circulo, rectangulo)

        # Dispara las funciones de colision.
        self.pilas.colisiones.actualizar()

    def testColisionesEntreEtiquetasDeFiguras(self):
        circulo = self.pilas.fisica.Circulo()
        rectangulo = self.pilas.fisica.Rectangulo(0, 0, 100, 100)

        def colisionan(figura1, figura2):
            self.assertEquals(figura1.id, circulo.id)
            self.assertEquals(figura2.id, rectangulo.id)

        self.pilas.colisiones.agregar("circulo", "rectangulo", colisionan)
        self.pilas.colisiones.notificar_colision(circulo, rectangulo)

        # Dispara las funciones de colision.
        self.pilas.colisiones.actualizar()


if __name__ == '__main__':
    unittest.main()
