# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class ListaSeleccion(Actor):

    def __init__(self, opciones, funcion_a_ejecutar, x=0, y=0):
        Actor.__init__(self, x=x, y=y)
        self.opciones = opciones
        self.funcion_a_ejecutar = funcion_a_ejecutar
        
        self.lienzo = pilas.lienzo.Lienzo(10, 10)
        ancho, alto = self.lienzo.obtener_area_para_lista_de_texto(opciones, tamano=14)
        self.lienzo = pilas.lienzo.Lienzo(int(ancho + 35), int(alto))
        self.lienzo.asignar(self)

        self._pintar_opciones()
        
        pilas.eventos.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        pilas.eventos.click_de_mouse.conectar(self.cuando_hace_click_con_el_mouse)
        self.centro = ("centro", "centro")
        
    def _pintar_opciones(self, pinta_indice_opcion=None):
        self.lienzo.deshabilitar_actualizacion_automatica()
        self.lienzo.pintar(pilas.colores.blanco)
        self.lienzo.definir_color(pilas.colores.negro)
        
        if pinta_indice_opcion != None:
            self.lienzo.definir_color(pilas.colores.naranja)
            self.lienzo.dibujar_rectangulo(0, pinta_indice_opcion * 19, 100, 17)
            self.lienzo.definir_color(pilas.colores.negro)
        
        for indice, opcion in enumerate(self.opciones):
            self.lienzo.escribir(opcion, 15, 12 + indice * 20, tamano=14)
            
        self.lienzo.habilitar_actualizacion_automatica()
        
    def cuando_mueve_el_mouse(self, evento):
        if self.colisiona_con_un_punto(evento.x, evento.y):
            opcion_seleccionada = self._detectar_opcion_bajo_el_mouse(evento)
            self._pintar_opciones(opcion_seleccionada)

    def cuando_hace_click_con_el_mouse(self, evento):
        if self.colisiona_con_un_punto(evento.x, evento.y):
            opcion = self._detectar_opcion_bajo_el_mouse(evento)
            self.funcion_a_ejecutar(self.opciones[opcion])

    def _detectar_opcion_bajo_el_mouse(self, evento):
        opcion = int((self.arriba - evento.y ) / 20)
        if opcion in range(0, len(self.opciones)):
            return opcion

