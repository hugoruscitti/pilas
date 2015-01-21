# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar



class Pad(object):

    def __init__(self, pilas):
        pass

    def actualizar(self):
        pass

    def hay_pads_conectados(self):
        return False
    
    def listar(self):
        pass
    
class PadDeshabilitado(object):

    def __init__(self, pilas):
        self.x = 0
        self.y = 0

        self.x1 = 0
        self.y1 = 0

        self.pilas = pilas
        self.joysticks = []
        self.pilas.log("Cargando el modulo de PAD deshabilitado")

    def actualizar(self):
        pass

    def hay_pads_conectados(self):
        pass

    def listar(self):
        pass



class PadHabilitado:

    def __init__(self, pilas):
        self.x = 0
        self.y = 0

        self.x1 = 0
        self.y1 = 0

        self.pilas = pilas
        self.joysticks = []

        self.pilas.log("Cargando el modulo de PAD deshabilitado")
        self.pilas.log("Inicializando pygame y el modulo de joystick")
        
        import pygame
        
        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        self.pilas.log("Obteniendo pads:", pygame.joystick.get_count())

        for i in range(0, pygame.joystick.get_count()):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
            self.joysticks.append(self.joystick)

    def listar(self):
        "Retorna una lista de todos los joysticks conectados"
        return [j.get_name().strip() for j in self.joysticks]

    def hay_pads_conectados(self):
        return len(self.joysticks) > 0

    def actualizar(self):
        import pygame
        if not self.hay_pads_conectados():
            return

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

    def emitir_evento_mueve_pad(self):
        self.pilas.escena.mueve_pad.emitir(x=self.x, y=self.y,
                                           x1=self.x1, y1=self.y1)
