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
        self.x = 0
        self.y = 0

        self.x1 = 0
        self.y1 = 0

        self.pilas = pilas
        self.joysticks = []

        pygame.joystick.init()
        pygame.init()

        self.joystick = None
        #print "Obteniendo pads:", pygame.joystick.get_count()


        for i in range(0, pygame.joystick.get_count()):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
            self.joysticks.append(self.joystick)
            #print self.joystick.get_name()
            #print "cantidad controles", self.joystick.get_numaxes()

    def listar(self):
        "Retorna una lista de todos los joysticks conectados"
        return [j.get_name().strip() for j in self.joysticks]


    def actualizar(self):

        def redondear(valor):
            if -0.2 < valor < 0.2:
                return 0
            else:
                return valor

        pygame.event.set_allowed([pygame.JOYAXISMOTION,
                                  pygame.JOYBALLMOTION,
                                  pygame.JOYHATMOTION,
                                  pygame.JOYBUTTONUP,
                                  pygame.JOYBUTTONDOWN
                                  ])

        for e in pygame.event.get():
            if e.type == pygame.JOYBUTTONDOWN:
                self.pilas.escena.pulsa_boton.emitir(numero=e.button)
            elif e.type == pygame.JOYAXISMOTION:
                if e.axis == 0:
                    self.x = redondear(e.value)
                    self.emitir_evento_mueve_pad()
                elif e.axis == 1:
                    self.y = redondear(-e.value)
                    self.emitir_evento_mueve_pad()
                elif e.axis == 2:
                    self.x1 = redondear(e.value)
                    self.emitir_evento_mueve_pad()
                elif e.axis == 3:
                    self.y1 = redondear(-e.value)
                    self.emitir_evento_mueve_pad()
            else:
                print e

    def emitir_evento_mueve_pad(self):
        self.pilas.escena.mueve_pad.emitir(x=self.x, y=self.y,
                                           x1=self.x1, y1=self.y1)