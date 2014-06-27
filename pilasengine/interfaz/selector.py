# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.interfaz import elemento

class Selector(elemento.Elemento):

    def __init__(self, pilas=None, texto='Sin Texto', x=0, y=0):
        super(Selector, self).__init__(pilas, x=x, y=y)
        self.x = x
        self.y = y
        self.z = -1000
        self.radio_de_colision = None
        self.texto = texto
        self.centro = ("centro", "centro")

        self._cargar_lienzo(200)
        self._cargar_imagenes()
        self.funcion_de_respuesta = None

        self.deseleccionar()
        self.pilas.escena.click_de_mouse.conectar(self.detection_click_mouse)

    def _cargar_imagenes(self):
        self.imagen_selector = self.pilas.imagenes.cargar("interfaz/selector.png")
        self.imagen_selector_seleccionado = self.pilas.imagenes.cargar("interfaz/selector_seleccionado.png")

    def _cargar_lienzo(self, ancho):
        self.imagen = self.pilas.imagenes.cargar_superficie(ancho, 29)

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

    def conectar(self, funcion):
        self.definir_accion(funcion)