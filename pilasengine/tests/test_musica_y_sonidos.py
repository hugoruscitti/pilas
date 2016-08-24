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
        musica = self.pilas.musica.cargar('audio/grito.wav')
        musica.reproducir()
        musica.detener()
        self.assertTrue('grito' in str(musica), "La musica se describe correctamente así: %s." %(str(musica)))

    def testPuedeCargarSonido(self):
        sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        sonido.reproducir()
        sonido.detener()
        self.assertTrue('grito' in str(sonido),
                        "El sonido se describe correctamente: %s." %(str(sonido)))

    def testPuedeDetenerGradualmente(self):
        sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        sonido.reproducir()
        sonido.detener_gradualmente(2)

        musica = self.pilas.musica.cargar('audio/grito.wav')
        musica.reproducir()
        musica.detener_gradualmente(2)
