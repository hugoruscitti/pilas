# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades


class EliminarseSiSaleDePantalla(habilidades.Habilidad):
    """Se asegura de que el actor sea eliminado si sale de los
    bordes de la pantalla.
    """
    def iniciar(self, receptor):
        """
        :param receptor: El actor que aprenderá la habilidad.
        """
        super(EliminarseSiSaleDePantalla, self).iniciar(receptor)
        self.ancho, self.alto = self.pilas.obtener_area()

    def actualizar(self):
        # Se asegura de regresar por izquierda y derecha.
        if self.receptor.derecha < -(self.ancho/2):
            self.eliminar_actor()
        elif self.receptor.izquierda > (self.ancho/2):
            self.eliminar_actor()

        # Se asegura de regresar por arriba y abajo.
        if self.receptor.abajo > (self.alto/2):
            self.eliminar_actor()
        elif self.receptor.arriba < -(self.alto/2):
            self.eliminar_actor()
            
    def eliminar_actor(self):
        self.receptor.eliminar()