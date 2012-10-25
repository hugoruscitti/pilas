# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


import pilas
from pilas.actores import Actor
from pilas.municion import BalaSimple


class Torreta(Actor):
    "Representa una torreta que puede disparar y rota con el mouse."

    def __init__(self, municion_bala_simple, enemigos, cuando_elimina_enemigo, x=0, y=0,
                 frecuencia_de_disparo=10):
        imagen = pilas.imagenes.cargar('torreta.png')
        Actor.__init__(self, imagen, x=x, y=y)

        self.radio_de_colision = 15

        if municion_bala_simple is None:
            municion_bala_simple = BalaSimple()

        self.aprender(pilas.habilidades.RotarConMouse,
                      lado_seguimiento=pilas.habilidades.RotarConMouse.ARRIBA)

        self.aprender(pilas.habilidades.DispararConClick,
                      municion_bala_simple=municion_bala_simple,
                      grupo_enemigos=enemigos,
                      cuando_elimina_enemigo=cuando_elimina_enemigo,
                      frecuencia_de_disparo=frecuencia_de_disparo,
                      angulo_salida_disparo=0,
                      offset_disparo=(27,27))

    def get_municion(self):
        return self.habilidades.DispararConClick.municion

    def set_municion(self, municion):
        self.habilidades.DispararConClick.municion = municion
        
    municion = property(get_municion, set_municion, doc="Define la munición de la torreta.")