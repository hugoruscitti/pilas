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

class Puntaje(Texto):
    """Representa un contador de Puntaje"""
	
    def __init__(self, texto='0', x=0, y=0, color=pilas.colores.negro):
        Texto.__init__(self, texto, x=x, y=y)
        self.color = color

    def definir(self, puntaje_variable = '0'):
        self.puntaje_texto = str(puntaje_variable)
        self.texto = self.puntaje_texto

    def aumentar(self, cantidad=1):
        self.definir(int(self.texto) + int(cantidad))
        
    def obtener(self):
        return int(self.texto)

