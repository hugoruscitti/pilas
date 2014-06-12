# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os


class Sonido(object):
    deshabilitado = False

    def __init__(self, ruta):
        import pygame

        self.ruta = ruta
        self.sonido = pygame.mixer.Sound(ruta)

    def reproducir(self, repetir=False):
        if repetir:
            self.sonido.play(-1)
        else:
            self.sonido.play()

    def detener(self):
        "Detiene el audio."
        self.sonido.stop()

    def pausar(self):
        "Hace una pausa del audio."
        self.sonido.stop()

    def continuar(self):
        "Continúa reproduciendo el audio."
        self.sonido.play()

    def __repr__(self):
        nombre = os.path.basename(self.ruta)
        return "<%s del archivo '%s'>" % (self.__class__.__name__, nombre)
