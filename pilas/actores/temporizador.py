# -*- encoding: utf-8 -*-
# For Pilas engine - A video game framework.
#
# Copyright 2010 - Pablo Garrido
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
#

import pilas
from pilas.actores import Texto

class Temporizador(Texto):
    def __init__(self, x=0, y=0, color=pilas.colores.negro):
        Texto.__init__(self, '0', x=x, y=y)
        self.ajustar(1, self.funcion_vacia)
        self.color = color


    # funcion cuando no se ajusta temporizador   
    def funcion_vacia(self):
        pass
    

    def definir_tiempo_texto(self, variable):
        self.texto = str(variable)


    # con la funcion ajustar manipulamos el tiempo y la
    # funcion queremos ejecutar
    def ajustar(self, tiempo = 1, funcion = None):

        self.tiempo = tiempo 
        self.definir_tiempo_texto(self.tiempo)

        if funcion == None:
            self.funcion = self.funcion_vacia()
        else:
            self.funcion = funcion



    # resta -1 hasta llegar a 0 el contador (numero en patalla)
    def restar_a_contador(self):
        if self.tiempo != 0:
            self.tiempo -= 1
            self.definir_tiempo_texto(self.tiempo)
            return True
   
    

    # iniciamos temporizador con respectivas funciones y tiempo ajustado
    def iniciar(self):
        pilas.mundo.agregar_tarea(self.tiempo, self.funcion)
        pilas.mundo.agregar_tarea(1, self.restar_a_contador)
        
        
        
    
    


