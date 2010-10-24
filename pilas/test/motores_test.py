# -*- encoding: utf-8 -*-
import random
import unittest
import pilas
from time import sleep as pausa

class AbstractTest():

    def test_creacion_de_ventana(self):
        self.motor.crear_ventana(320, 240, "test")
        pausa(1)
    

class TestPygameMotor(unittest.TestCase, AbstractTest):
    "Verifica que todas las llamadas a pygame funcionan correctamente."

    def setUp(self):
        self.motor = pilas.motores.Pygame()

class TestPySFMLMotor(unittest.TestCase, AbstractTest):
    "Verifica que todas las llamadas a pySFML funcionan correctamente."

    def setUp(self):
        self.motor = pilas.motores.pySFML()

if __name__ == '__main__':
    unittest.main()
