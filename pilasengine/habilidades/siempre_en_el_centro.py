# -*- encoding: utf-8 -*-

from pilasengine.habilidades.habilidad import Habilidad

class SiempreEnElCentro(Habilidad):
    """Hace que un actor siempre esté en el centro de la camara y la desplace
    cuando el actor se desplaza."""

    def iniciar(self, receptor):
    	Habilidad.iniciar(self, receptor)

    def actualizar(self):
        self.pilas.escena_actual().camara.x = self.receptor.x
        self.pilas.escena_actual().camara.y = self.receptor.y

    def eliminar(self):
    	Habilidad.eliminar(self)