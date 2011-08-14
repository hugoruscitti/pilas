# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class CursorMano(Actor):
    "Representa un bloque que tiene fisica como una caja."

    def __init__(self, x=0, y=0):
        self._cargar_imagenes()
        Actor.__init__(self, self.imagen_normal)
        self.x = x
        self.y = y

        self.aprender(pilas.habilidades.SeguirAlMouse)
        pilas.mundo.motor.ocultar_puntero_del_mouse()
        self.z = -200
        self.pulsado = False
        
        self.centro = ("izquierda", "arriba")

        pilas.eventos.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        pilas.eventos.click_de_mouse.conectar(self.cuando_pulsa_el_mouse)
        pilas.eventos.termina_click.conectar(self.cuando_suelta_el_mouse)

    def _cargar_imagenes(self):
        self.imagen_normal = pilas.imagenes.cargar("cursores/normal.png")
        self.imagen_arrastrando = pilas.imagenes.cargar("cursores/arrastrando.png")

    def cuando_pulsa_el_mouse(self, evento):
        self.pulsado = True

    def cuando_mueve_el_mouse(self, evento):
        if self.pulsado:
            self.imagen = self.imagen_arrastrando

    def cuando_suelta_el_mouse(self, evento):
        if self.pulsado:
            self.imagen = self.imagen_normal
            self.pulsado = False
