# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor



class Bala(Actor):
    """ Representa una bala que va en línea recta. """

    def __init__(self, pilas, x=0, y=0, rotacion=0, velocidad_maxima=9,
                 angulo_de_movimiento=90):

        """
        Construye la Bala.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        super(Bala, self).__init__(pilas=pilas, x=x, y=y)
        self.imagen = pilas.imagenes.cargar('disparos/bola_amarilla.png')
        self.rotacion = rotacion

        self.radio_de_colision = 5

        self.hacer(pilas.comportamientos.Proyectil,
                   velocidad_maxima=velocidad_maxima,
                   aceleracion=1,
                   angulo_de_movimiento=angulo_de_movimiento,
                   gravedad=0)

        self.aprender(self.pilas.habilidades.EliminarseSiSaleDePantalla)
        self.cuando_se_elimina = None

    def eliminar(self):
        if self.cuando_se_elimina:
            self.cuando_se_elimina(self)

        super(Bala, self).eliminar()
