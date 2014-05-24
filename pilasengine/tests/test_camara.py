# -*- encoding: utf-8 -*-
import unittest

import pilasengine


class TestCamara(unittest.TestCase):

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeMoverLaCamara(self):
        self.assertEqual(0, self.pilas.camara.x, "La cámara esta en el centro")
        self.assertEqual(0, self.pilas.camara.y, "La cámara esta en el centro")

    def testPuedeVibrar(self):
        self.pilas.camara.vibrar()


if __name__ == '__main__':
    unittest.main()