# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import actores


class CursorDisparo(actores.Actor):

    def iniciar(self):
        self.imagen = self.pilas.imagenes.cargar('cursordisparo.png')
        self.rotacion = 0
        self.radio_de_colision = 25

        self.aprender(self.pilas.habilidades.SeguirAlMouse)
        self.pilas.ocultar_puntero_del_mouse()