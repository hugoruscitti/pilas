# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades

import random

class SeguirAOtroActor(habilidades.Habilidad):
    "Hace que un actor siga a otro actor."

    def iniciar(self, receptor, actor_a_seguir, velocidad=5, inteligencia=1):
        super(SeguirAOtroActor, self).iniciar(receptor)
        self.objetivo = actor_a_seguir
        self.velocidad = velocidad
        self.inteligencia = 1
        self.perdido = None

    def actualizar(self):

        def limitar(valor):
            return min(max(valor, -self.velocidad), self.velocidad)

        objetivo_x = self.objetivo.x
        objetivo_y = self.objetivo.y

        if self.inteligencia == 0:

            if self.perdido:
                # perdido, continua persiguiendo una posicion antigua
                ( objetivo_x, objetivo_y ) = self.perdido
                 
                if random.randint(0, 10) > 7:
                    # no se pierde mas
                    self.perdido = None
                    
            elif random.randint(0, 10) > 7:
                # se pierde
                self.perdido = ( self.objetivo.x, self.objetivo.y )

        self.receptor.x += limitar(objetivo_x - self.receptor.x)
        self.receptor.y += limitar(objetivo_y - self.receptor.y)
