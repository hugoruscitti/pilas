# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pygame
from PySFML import sf
from pilas.simbolos import *


class Pygame:

    def __init__(self):
        pygame.init()

    def crear_ventana(self, ancho, alto, titulo):
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(titulo)
        return self.ventana


    def centrar_ventana(self):
        pass


    def pulsa_tecla(self, tecla):
        "Indica si una tecla esta siendo pulsada en este instante."

        mapa = {
                IZQUIERDA: pygame.K_LEFT,
                DERECHA: pygame.K_RIGHT,
                ARRIBA: pygame.K_UP,
                ABAJO: pygame.K_DOWN,
                BOTON: pygame.K_SPACE,
                }

        return pygame.key.get_pressed()[mapa[tecla]]


class pySFML:

    def __init__(self):
        pass

    def crear_ventana(self, ancho, alto, titulo):
        ventana = sf.RenderWindow(sf.VideoMode(ancho, alto), titulo)
        # Define que la coordenada (0, 0) sea el centro de la ventana.
        view = ventana.GetDefaultView()
        view.SetCenter(0, 0)
        self.input = ventana.GetInput()
        self.ventana = ventana
        return ventana

    def pulsa_tecla(self, tecla):
        "Indica si una tecla esta siendo pulsada en este instante."

        mapa = {
                IZQUIERDA: sf.Key.Left,
                DERECHA: sf.Key.Right,
                ARRIBA: sf.Key.Up,
                ABAJO: sf.Key.Down,
                BOTON: sf.Key.Space,
                }

        return self.input.IsKeyDown(mapa[tecla])


    def centrar_ventana(self):
        "Coloca la ventana principal en el centro del escritorio."

        vm = sf.VideoMode(100, 100)

        # Obtiene la resolución del escritorio y la ventana.
        desktop_mode = vm.GetDesktopMode()
        w, h = self.ventana.GetWidth(), self.ventana.GetHeight()

        # Calcula cual debería la coordenada para centrar la ventana.
        to_x = desktop_mode.Width/2 - w/2
        to_y = desktop_mode.Height/2 - h/2

        self.ventana.SetPosition(to_x, to_y)
