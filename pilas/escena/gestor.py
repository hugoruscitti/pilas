# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


class Gestor(object):

    
    def __init__(self):
        # Pila para almacenar las escenas.
        self.escenas = []
                        
    
    def limpiar (self):
        while len(self.escenas) > 0:
            escena = self.escenas.pop()
            escena.limpiar()

    def cambiar_escena (self, escena):
        if len(self.escenas) > 0:
            escena = self.escenas.pop()
            escena.limpiar()
        
        self.escenas.append(escena)
        self.escenas[-1].iniciar()

    def almacenar_escena(self, escena):
        if len(self.escenas) > 0:
            self.escenas[-1].pausar()

        self.escenas.append(escena)
        self.escenas[-1].iniciar()

    def recuperar_escena(self):
        if len(self.escenas) > 0:
            escena = self.escenas.pop()
            escena.limpiar()

        if len(self.escenas) > 0:
            self.escenas[-1].reanudar()

    def escena_actual(self):
        return self.escenas[-1]

    def gestionar_eventos(self, events):
        self.escenas[-1].gestionarEventos(events)

    def actualizar(self):
        self.escenas[-1].actualizar()

    def dibujar(self):
        self.escenas[-1].dibujar()

    def salir(self):
        print "Quit"            
    
