# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Animacion


class Nave(Animacion):
    """Representa una nave que puede disparar.

    .. image:: images/actores/nave.png

    """

    def __init__(self, x=0, y=0, velocidad=2):
        """
        Constructor de la Nave.

        :param x: posicion horizontal de la nave.
        :type x: int
        :param y: posicion vertical de la nave.
        :type y: int
        :param velocidad: Velocidad que llevará la nave.
        :type velocidad: int

        """
        self.velocidad = velocidad
        grilla = pilas.imagenes.cargar_grilla("nave.png", 2)
        Animacion.__init__(self, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = 20
        self.aprender(pilas.habilidades.PuedeExplotar)

        self.municion = pilas.actores.proyectil.Misil
        self.aprender(pilas.habilidades.Disparar,
                       municion=self.municion,
                       angulo_salida_disparo=0,
                       frecuencia_de_disparo=3,
                       offset_disparo=(29,29),
                       escala=0.7)

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
        """Hace que una nave tenga como enemigos a todos los actores del grupo.

        :param grupo: El grupo de actores que serán sus enemigos.
        :type grupo: array
        :param cuando_elimina_enemigo: Funcion que se ejecutará cuando se elimine un enemigo.

        """
        self.cuando_elimina_enemigo = cuando_elimina_enemigo
        self.habilidades.Disparar.definir_colision(grupo, self.hacer_explotar_al_enemigo)

    def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
        """Es el método que se invoca cuando se produce una colisión 'tiro <-> enemigo'

        :param mi_disparo: El disparo de la nave.
        :param el_enemigo: El enemigo que se eliminará.
        """
        mi_disparo.eliminar()
        el_enemigo.eliminar()

        if self.cuando_elimina_enemigo:
            self.cuando_elimina_enemigo()

    def disparar(self):
        for x in self._habilidades:
            if x.__class__.__name__ == 'Disparar':
                x.disparar()
