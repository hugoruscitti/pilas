# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class Aceituna(Actor):

    def __init__(self, x=0, y=0):
        self.cuadro_normal = pilas.imagenes.cargar("aceituna.png")
        self.cuadro_reir = pilas.imagenes.cargar("aceituna_risa.png")
        self.cuadro_burla = pilas.imagenes.cargar("aceituna_burla.png")
        self.cuadro_grita = pilas.imagenes.cargar("aceituna_grita.png")

        Actor.__init__(self, x=x, y=y)
        self.imagen = self.cuadro_normal
        self.centro = ('centro', 'centro')
        self.radio_de_colision = 18

    def normal(self):
        self.imagen = self.cuadro_normal

    def reir(self):
        self.imagen = self.cuadro_reir

    def burlarse(self):
        self.imagen = self.cuadro_burla

    burlar = burlarse

    def gritar(self):
        self.imagen = self.cuadro_grita

    def saltar(self):
        self.hacer(pilas.comportamientos.Saltar())
