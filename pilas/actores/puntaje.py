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
        """Inicializa el Puntaje.

        :param texto: El número inicial del puntaje.
        :param x: Posición horizontal para el puntaje.
        :param y: Posición vertical para el puntaje.
        :param color: Color que tendrá el texto de puntaje.
        """
        Texto.__init__(self, str(texto), x=x, y=y)
        self.color = color
        self.valor = int(texto)

    def definir(self, puntaje_variable = '0'):
        """Cambia el texto que se mostrará cómo puntaje.

        :param puntaje_variable: Texto a definir.
        """
        self.valor = int(puntaje_variable)
        self.texto = str(self.valor)

    def aumentar(self, cantidad=1):
        """Incrementa el puntaje.

        :param cantidad: La cantidad de puntaje que se aumentará.
        """
        self.definir(self.valor + int(cantidad))

    def reducir(self, cantidad=1):
        """Reduce el puntaje.

        :param cantidad: La cantidad de puntaje que se reducirá.
        """
        self.definir(self.valor - int(cantidad))

    def obtener(self):
        """Retorna el puntaje en forma de número."""
        return self.valor
