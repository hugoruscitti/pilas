# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.animacion import Animacion


class Dinamita(Animacion):

    def __init__(self, pilas, *k, **kv):
        Animacion.__init__(self, pilas, *k, **kv)

    def pre_iniciar(self,x=0,y=0,rotacion=0,velocidad_maxima=4, angulo_de_movimiento=90):
        """
        Construye la Dinamita.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param rotacion: Angulo de rotación del Actor.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        grilla = self.pilas.imagenes.cargar_grilla("disparos/dinamita.png", 2)
        Animacion.pre_iniciar(self, grilla, ciclica=True, x=x, y=y, velocidad=40)
        self.rotacion = rotacion
        self.radio_de_colision = 20

        self.hacer(self.pilas.comportamientos.Proyectil, velocidad_maxima=velocidad_maxima,
                                                   aceleracion=0.4,
                                                   angulo_de_movimiento=angulo_de_movimiento,
                                                   gravedad=3)
        self.escala = 0.7

        self.aprender("PuedeExplotar")

    def actualizar(self):
        self.rotacion += 3
        Animacion.actualizar(self)


