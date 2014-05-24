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
        musica = self.pilas.musica.cargar('audio/musica.mp3')
        musica.reproducir()
        musica.detener()
        self.assertTrue('musica' in str(musica),
                        "El sonido se describe correctamente.")

    def testPuedeCargarSonido(self):
        sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        sonido.reproducir()
        sonido.detener()
        self.assertTrue('grito' in str(sonido),
                        "El sonido se describe correctamente.")