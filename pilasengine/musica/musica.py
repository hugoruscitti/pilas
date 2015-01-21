# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os

class Musica(object):
    deshabilitado = False

    def __init__(self, ruta):
        import pygame

        self.ruta = ruta
        self.musica = pygame.mixer.music.load(ruta)

    def reproducir(self, repetir=False):
        import pygame

        if repetir:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    def detener(self):
        "Detiene el audio."
        import pygame

        pygame.mixer.music.stop()

    def pausar(self):
        "Hace una pausa del audio."
        import pygame

        pygame.mixer.music.stop()

    def continuar(self):
        "Continúa reproduciendo el audio."
        import pygame

        pygame.mixer.music.play()

    def __repr__(self):
        nombre = os.path.basename(self.ruta)
        return "<%s del archivo '%s'>" % (self.__class__.__name__, nombre)


class MusicaDeshabilitada(object):

    def __init__(self, ruta):
        self.ruta = ruta
        
    def reproducir(self, repetir=False):
        pass

    def detener(self):
        pass

    def pausar(self):
        pass

    def continuar(self):
        pass
    
    def __repr__(self):
        nombre = os.path.basename(self.ruta)
        return "<%s del archivo '%s'>" % (self.__class__.__name__, nombre)

