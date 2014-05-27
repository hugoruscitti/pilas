# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import actores


class EstrellaNinja(actores.Actor):
    """ Representa una estrella ninja. """

    def iniciar(self):
        self.imagen = self.pilas.imagenes.cargar('disparos/estrella.png')
        self.rotacion = 0
        self.escala = 0.5
        self.radio_de_colision = 20

        ## TODO: buscar la forma de poder cambiar la velocidad y el angulo
        ## de movimiento desde esta clase.
        self.hacer(self.pilas.comportamientos.Proyectil, velocidad_maxima=1,
                                                    aceleracion=1,
                                                    angulo_de_movimiento=0,
                                                    gravedad=0)

    def actualizar(self):
        self.rotacion += 10