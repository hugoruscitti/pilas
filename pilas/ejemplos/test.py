# -*- encoding: utf-8 -*-
import random
import unittest
import pilas

class MockEscena:

    def __init__(self):
        self.grupos = {1: [],
                       8: []}

class TestPiezas(unittest.TestCase):

    def test_pieza_de_ejemplo(self):

        filas = 3
        columnas = 3

        mock_escena = MockEscena()

        grilla = pilas.imagenes.Grilla("ejemplos/data/piezas.png", filas, columnas)
        p = pilas.ejemplos.piezas.Pieza(mock_escena, grilla, 1, filas, columnas)

        self.assertEqual(p.numero, 1)
        self.assertEqual(p.numero_derecha, 2)
        self.assertEqual(p.numero_izquierda, 0)
        self.assertTrue(p.numero_arriba < 0)
        self.assertEqual(p.numero_abajo, 4)

        p = pilas.ejemplos.piezas.Pieza(mock_escena, grilla, 8, filas, columnas)

        self.assertEqual(p.numero, 8)
        self.assertEqual(p.numero_derecha, -1)   # la pieza 8 no tiene borde derecho.
        self.assertEqual(p.numero_izquierda, 7) 
        self.assertEqual(p.numero_arriba, 5)
        self.assertEqual(p.numero_abajo, 11) # la pieza 8 no tiene parte de abajo

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
