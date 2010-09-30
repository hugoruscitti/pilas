# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor, BaseActor
from PySFML import sf


class Texto(sf.String, BaseActor):
    """Representa un texto en pantalla.

    El texto tiene atributos como ``texto``, ``magnitud`` y ``color``.
    """

    def __init__(self, text="None"):
        sf.String.__init__(self, text)
        self.color = (0, 0, 0)
        BaseActor.__init__(self)

    def get_text(self):
        return self.GetText()

    def set_text(self, text):
        self.SetText(text)

    def get_size(self):
        return self.GetSize()

    def set_size(self, size):
        self.SetSize(size)
        self._set_central_axis()

    def _set_central_axis(self):
        rect = self.GetRect()
        size = (rect.GetWidth(), rect.GetHeight())
        self.SetCenter(size[0]/2, size[1]/2)

    def get_color(self):
        c = self.GetColor()
        return (c.r, c.g, c.b, c.a)

    def set_color(self, k):
        self.SetColor(sf.Color(*k))

    texto = property(get_text, set_text, doc="El texto que se tiene que mostrar.")
    magnitud = property(get_size, set_size, doc="El tamaño del texto.")
    color = property(get_color, set_color, doc="Color del texto.")

    def dibujar(self, aplicacion):
        aplicacion.Draw(self)

    def colisiona_con_un_punto(self, x, y):
        return False
