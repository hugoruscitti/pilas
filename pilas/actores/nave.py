# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion
import math

class Nave(Animacion):
    "Representa una nave que puede disparar."

    def __init__(self, x=0, y=0, velocidad=2):
        self.velocidad = velocidad
        grilla = pilas.imagenes.cargar_grilla("nave.png", 2)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = 20
        self.aprender(pilas.habilidades.PuedeExplotar)

        self.aprender(pilas.habilidades.Disparar,
                       actor_disparado=pilas.actores.Disparo,
                       angulo_salida_disparo=90,
                       frecuencia_de_disparo=5,
                       offset_disparo=(20,20),
                       velocidad=4)

        self.aprender(pilas.habilidades.MoverseConElTeclado,
                      velocidad_maxima=self.velocidad,
                      aceleracion=1,
                      deceleracion=0.04,
                      con_rotacion=True,
                      velocidad_rotacion=1,
                      marcha_atras=False)

    def actualizar(self):
        Animacion.actualizar(self)

    def definir_enemigos(self, grupo, cuando_elimina_enemigo=None):
        """hace que una nave tenga como enemigos a todos los actores del grupo.

        El argumento cuando_elimina_enemigo tiene que ser una funcion que
        se ejecutara cuando se produzca la colision."""
        self.cuando_elimina_enemigo = cuando_elimina_enemigo
        self.habilidades.Disparar.definir_colision(grupo, self.hacer_explotar_al_enemigo)

    def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
        "Es el método que se invoca cuando se produce una colisión 'tiro <-> enemigo'"
        mi_disparo.eliminar()
        el_enemigo.eliminar()

        if self.cuando_elimina_enemigo:
            self.cuando_elimina_enemigo()
