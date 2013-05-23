# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
#
# Deslizador creado por Pablo Garrido

import pilas
from pilas.interfaz.base_interfaz import BaseInterfaz

class Selector(BaseInterfaz):
    """Representa un selector con un checkbox."""

    def __init__(self, texto, x=0, y=0, ancho=200):
        """Inicializa el selector.

        :param texto: Texto que se mostrará junto al selector.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param ancho: Ancho del selector.
        """
        BaseInterfaz.__init__(self, x=x, y=y)

        self.texto = texto
        self._cargar_lienzo(ancho)
        self._cargar_imagenes()
        self.funcion_de_respuesta = None

        self.deseleccionar()
        self.escena.click_de_mouse.conectar(self.detection_click_mouse)
        self.fijo = True

    def _cargar_imagenes(self):
        self.imagen_selector = pilas.imagenes.cargar("interfaz/selector.png")
        self.imagen_selector_seleccionado = pilas.imagenes.cargar("interfaz/selector_seleccionado.png")

    def _cargar_lienzo(self, ancho):
        self.imagen = pilas.imagenes.cargar_superficie(ancho, 29)

    def pintar_texto(self):
        "Dibuja el texto sobre el selector."
        self.imagen.texto(self.texto, 35, 10)

    def deseleccionar(self):
        "Destilda el selector."
        self.seleccionado = False
        self.imagen.limpiar()
        self.imagen.pintar_imagen(self.imagen_selector)
        self.pintar_texto()
        self.centro = ("centro", "centro")

    def seleccionar(self):
        "Tilda el selector."
        self.seleccionado = True
        self.imagen.limpiar()
        self.imagen.pintar_imagen(self.imagen_selector_seleccionado)
        self.pintar_texto()
        self.centro = ("centro", "centro")

    def detection_click_mouse(self, click):
        """Detecta el click de mouse y alterna la selección.

        :param click: representa el evento de click.
        """
        if (self.activo):
            if self.colisiona_con_un_punto(click.x, click.y):
                self.alternar_seleccion()

    def alternar_seleccion(self):
        """Alterna la selección del selector."""
        if self.seleccionado:
            self.deseleccionar()
        else:
            self.seleccionar()

        if self.funcion_de_respuesta:
            self.funcion_de_respuesta(self.seleccionado)

    def definir_accion(self, funcion):
        """Define cual será la función a ejecutar en la selección.

        :param funcion: La función a ejecutar.
        """
        self.funcion_de_respuesta = funcion
