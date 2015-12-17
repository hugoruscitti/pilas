# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui

import pilasengine


class TestMusicaYSonidos(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCargarMusica(self):
        datos = self.pilas.datos.generar('mi_juego')

        datos.guardar('mejor_puntaje', 100)
        dato = datos.obtener('mejor_puntaje')

        self.assertTrue(dato is 100)

        datos.guardar('datos', [1, 2, 3, 4])
        dato = datos.obtener('datos')

        self.assertTrue(dato == [1, 2, 3, 4])

        datos.guardar('nombre', "Don pepe")
        nombre_del_jugador = datos.obtener('nombre')

        self.assertEqual(nombre_del_jugador, "Don pepe")

    def testPuedeCargarSonido(self):
        sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        sonido.reproducir()
        sonido.detener()
        self.assertTrue('grito' in str(sonido),
                        "El sonido se describe correctamente: %s." %(str(sonido)))
