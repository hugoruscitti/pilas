# -*- encoding: utf-8 -*-
import random
import unittest
import pilas
from time import sleep as pausa

class AbstractTest():

    def iniciar(self):
        self.motor.crear_ventana(320, 240, "test")
        self.motor.centrar_ventana()

        # A partir de ahora todas las llamadas internas de
        # pilas se delegan en este motor.
        pilas.motor = self.motor

    def test_creacion_de_ventana(self):
        self.iniciar()

    def test_control(self):
        self.iniciar()

        c = pilas.control.Control()
        c.actualizar()

        self.assertFalse(c.izquierda)
        self.assertFalse(c.derecha)
        
    def test_camara(self):
        pass


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
