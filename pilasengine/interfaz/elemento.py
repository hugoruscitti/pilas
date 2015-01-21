# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.actores import actor

class Elemento(actor.Actor):

    def __init__(self, pilas=None, x=0, y=0):
        super(Elemento, self).__init__(pilas, x=x, y=y)
        self.z = -1000
        self.radio_de_colision = None

        self.tiene_el_foco = False
        self.pilas.escena_actual().click_de_mouse.conectar(self.cuando_hace_click)

        self._visible = True

        self.activo = True

    def obtener_foco(self):
        "Retorna True si el actor tiene foco."
        self.tiene_el_foco = True

    def perder_foco(self):
        "Quita el foco sobre el elemento."
        self.tiene_el_foco = False

    def cuando_hace_click(self, evento):
        """Se encarga de atender el evento click y conseguir foco."""
        if self._visible:
            if self.colisiona_con_un_punto(evento.x, evento.y):
                self.obtener_foco()
            else:
                self.perder_foco()

    def ocultar(self):
        """Oculta el elemento de la interfaz."""
        self.transparencia = 100
        self._visible = False
        self.activo = False

    def mostrar(self):
        """Muestra el elemento."""
        self._visible = True
        self.activar()

    def activar(self):
        self.activo = True
        self.transparencia = 0

    def desactivar(self):
        self.activo = False
        self.transparencia = 50
