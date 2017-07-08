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
        self.ruta = ruta

        if not Musica.deshabilitado:
            import pygame
            pygame.mixer.init()
            self.musica = pygame.mixer.music.load(ruta)

    def reproducir(self, repetir=False):
        if not Musica.deshabilitado:
            import pygame

            if repetir:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()

    def detener(self):
        "Detiene el audio."
        if not Musica.deshabilitado:
            import pygame
            pygame.mixer.music.stop()

    def pausar(self):
        "Hace una pausa del audio."
        if not Musica.deshabilitado:
            import pygame
            pygame.mixer.music.stop()

    def continuar(self):
        "Continúa reproduciendo el audio."
        if not Musica.deshabilitado:
            import pygame
            pygame.mixer.music.play()

    def __repr__(self):
        nombre = os.path.basename(self.ruta)

        if Musica.deshabilitado:
            return "<%s Deshabilita, del archivo '%s'>" % (self.__class__.__name__, nombre)
        else:
            return "<%s del archivo '%s'>" % (self.__class__.__name__, nombre)

    def detener_gradualmente(self, segundos=2):
        if not Musica.deshabilitado:
            import pygame
            pygame.mixer.music.fadeout(segundos * 1000)

class MusicaDeshabilitada(object):

    def __init__(self, ruta):
        self.ruta = ruta

    def reproducir(self, repetir=False):
        pass

    def detener(self):
        pass

    def detener_gradualmente(self, segundos=2):
        pass

    def pausar(self):
        pass

    def continuar(self):
        pass

    def __repr__(self):
        nombre = os.path.basename(self.ruta)
        return "<%s deshabilitada del archivo '%s'>" % (self.__class__.__name__, nombre)
