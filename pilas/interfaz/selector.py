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

class Selector(pilas.actores.Actor):
    
    def __init__(self, texto, x=0, y=0, ancho=200):
        pilas.actores.Actor.__init__(self, x=x, y=y)
        
        self.texto = texto
        self._cargar_lienzo(ancho)
        self._cargar_imagenes()
        self.funcion_de_respuesta = None

        self.deseleccionar()
        pilas.eventos.click_de_mouse.conectar(self.detection_click_mouse)

    def _cargar_imagenes(self):
        self.imagen_selector = pilas.imagenes.cargar("interfaz/selector.png")
        self.imagen_selector_seleccionado = pilas.imagenes.cargar("interfaz/selector_seleccionado.png")

    def _cargar_lienzo(self, ancho):
        self.imagen = pilas.imagenes.cargar_superficie(ancho, 29)
        
    def pintar_texto(self):
        self.imagen.texto(self.texto, 35, 20)
        
    def deseleccionar(self):
        self.seleccionado = False
        self.imagen.limpiar()
        self.imagen.pintar_imagen(self.imagen_selector)
        self.pintar_texto()
        self.centro = ("centro", "centro")
        
    def seleccionar(self):
        self.seleccionado = True
        self.imagen.limpiar()
        self.imagen.pintar_imagen(self.imagen_selector_seleccionado)
        self.pintar_texto()
        self.centro = ("centro", "centro")
                
    def detection_click_mouse(self, click):
        if self.colisiona_con_un_punto(click.x, click.y):
            self.alternar_seleccion()
                
    def alternar_seleccion(self):
        if self.seleccionado:
            self.deseleccionar()
        else:
            self.seleccionar()

        if self.funcion_de_respuesta:
            self.funcion_de_respuesta(self.seleccionado)

    def definir_accion(self, funcion):
        self.funcion_de_respuesta = funcion
