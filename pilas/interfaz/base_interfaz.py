# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class BaseInterfaz(pilas.actores.Actor):
    
    def __init__(self, imagen="sin_imagen.png",x=0, y=0):
        pilas.actores.Actor.__init__(self, imagen=imagen, x=x, y=y)

        self.tiene_el_foco = False
        self.escena.click_de_mouse.conectar(self.cuando_hace_click)
        
        self._visible = True
        
        self.activo = True
    
    def obtener_foco(self):
        self.tiene_el_foco = True
    
    def perder_foco(self):
        self.tiene_el_foco = False

    def cuando_hace_click(self, evento):
        if (self._visible):
            if self.colisiona_con_un_punto(evento.x, evento.y):
                self.obtener_foco()
            else:
                self.perder_foco()
            
    def ocultar(self):
        self.transparencia = 100
        self._visible = False
        self.activo = False
        
    def mostrar(self):
        self._visible = True
        self.activar()
        
    def activar(self):
        self.activo = True
        self.transparencia = 0
        
    def desactivar(self):
        self.activo = False
        self.transparencia = 50