# -*- encoding: utf-8 -*-
# For Pilas engine - A video game framework.
#
# Copyright 2010 - Pablo Garrido
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
#

import pilas
from puntaje import Puntaje

class Temporizador(Puntaje):
    
    def __init__(self, x=0, y=0, color = pilas.colores.negro):
        
        self.Puntaje = Puntaje('0', x, y, color)
        self.ajustar(1, self.funcion_vacia)
     
    # funcion cuando no se ajusta temporizador   
    def funcion_vacia(self):
        pass
    

    # con la funcion ajustar manipulamos el tiempo y la
    # funcion queremos ejecutar
    def ajustar(self, tiempo = 1, funcion = None):
        self.Puntaje.definir(tiempo)
        self.tiempo = tiempo
        if funcion == None:
            self.funcion = self.funcion_vacia()
        else:
            self.funcion = funcion

    
    
    # resta -1 hasta llegar a 0 el contador (numero en patalla)
    def restar_a_contador(self):
        if self.Puntaje.obtener() <= 0:
            return False
        else:
            self.Puntaje.aumentar(-1)
            return True
        
    
    # iniciamos temporizador con respectivas funciones y tiempo ajustado
    def iniciar(self):
        pilas.mundo.agregar_tarea(1, self.restar_a_contador)
        pilas.mundo.agregar_tarea(self.tiempo,self.funcion)
        
    
    


