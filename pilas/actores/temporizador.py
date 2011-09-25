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
from pilas import colores

class Temporizador(Texto):
    """Representa un contador de tiempo con cuenta regresiva.

    Por ejemplo:

        >>> t = pilas.actores.Temporizador()
        >>> def hola_mundo():
        ...     pilas.avisar("Hola mundo, pasaron 10 segundos...")
        ... 
        >>> t.ajustar(10, hola_mundo)
        >>> t.iniciar()

    """
    def __init__(self, x=0, y=0, color=colores.negro):
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
    def ajustar(self, tiempo=1, funcion=None):
        """Indica una funcion para ser invocada en el tiempo indicado.

        La función no tiene que recibir parámetros, y luego de
        ser indicada se tiene que iniciar el temporizador. 
        """

        self.tiempo = tiempo 
        self.definir_tiempo_texto(self.tiempo)

        if funcion == None:
            self.funcion = self.funcion_vacia()
        else:
            self.funcion = funcion

    def _restar_a_contador(self):
        if self.tiempo != 0:
            self.tiempo -= 1
            self.definir_tiempo_texto(self.tiempo)
            return True
    
    def iniciar(self):
        """Inicia el contador de tiempo con la función indicada."""
        pilas.mundo.agregar_tarea_una_vez(self.tiempo, self.funcion)
        pilas.mundo.agregar_tarea_siempre(1, self._restar_a_contador)
        
