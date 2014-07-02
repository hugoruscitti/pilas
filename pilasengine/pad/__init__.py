# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pygame

class Pad:

    def __init__(self, pilas):
        self.pilas = pilas
        pygame.init()
        self.joystick = None

        for i in range(0, pygame.joystick.get_count()):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()

        self.x = 0
        self.y = 0

        self.x1 = 0
        self.y1 = 0

    def actualizar(self):

        def redondear(valor):
            if -0.2 < valor < 0.2:
                return 0
            else:
                return valor

        for e in pygame.event.get():
            if e.type == pygame.JOYBUTTONDOWN:
                self.pilas.escena.pulsa_boton.emitir(numero=e.button)
            elif e.type == pygame.JOYAXISMOTION:
                if e.axis == 0:
                    self.x = redondear(e.value)
                elif e.axis == 1:
                    self.y = redondear(-e.value)
                elif e.axis == 2:
                    self.x1 = redondear(e.value)
                elif e.axis == 3:
                    self.y1 = redondear(-e.value)
