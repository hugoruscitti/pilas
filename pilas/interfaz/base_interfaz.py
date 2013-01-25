# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class BaseInterfaz(pilas.actores.Actor):
    """Representa un actor que actuará como un elemento de interfaz de usuario."""

    def __init__(self, imagen="sin_imagen.png",x=0, y=0):
        """Inicializa al actor.

        :param imagen: Imagen inicial.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        """
        pilas.actores.Actor.__init__(self, imagen=imagen, x=x, y=y)

        self.tiene_el_foco = False
        self.escena.click_de_mouse.conectar(self.cuando_hace_click)

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
