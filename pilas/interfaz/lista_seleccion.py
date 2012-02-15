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

    def __init__(self, opciones, funcion_a_ejecutar=None, x=0, y=0):
        Actor.__init__(self, x=x, y=y)
        self.opciones = opciones
        self.funcion_a_ejecutar = funcion_a_ejecutar
        
        ancho, alto = pilas.mundo.motor.obtener_area_de_texto("\n".join(opciones))
        self.imagen = pilas.imagenes.cargar_superficie(int(ancho + 35), int(alto + 5))

        self._pintar_opciones()
        
        pilas.eventos.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        pilas.eventos.click_de_mouse.conectar(self.cuando_hace_click_con_el_mouse)
        self.centro = ("centro", "centro")
        self.fijo = True
        
    def _pintar_opciones(self, pinta_indice_opcion=None):
        self.imagen.pintar(pilas.colores.blanco)
        
        if pinta_indice_opcion != None:
            self.imagen.rectangulo(0, pinta_indice_opcion * 19, self.imagen.ancho(), 17, relleno=True, color=pilas.colores.naranja)
        
        for indice, opcion in enumerate(self.opciones):
            self.imagen.texto(opcion, 15, y=12 + indice * 20, color=pilas.colores.negro)
        
    def cuando_mueve_el_mouse(self, evento):
        if self.colisiona_con_un_punto(evento.x, evento.y):
            opcion_seleccionada = self._detectar_opcion_bajo_el_mouse(evento)
            self._pintar_opciones(opcion_seleccionada)

    def cuando_hace_click_con_el_mouse(self, evento):
        if self.colisiona_con_un_punto(evento.x, evento.y):
            opcion = self._detectar_opcion_bajo_el_mouse(evento)
            if self.funcion_a_ejecutar:
                self.funcion_a_ejecutar(self.opciones[opcion])
            else:
                print "Cuidado, no has definido funcion a ejecutar en la lista de seleccion."

    def _detectar_opcion_bajo_el_mouse(self, evento):
        opcion = int((self.arriba - evento.y ) / 20)
        if opcion in range(0, len(self.opciones)):
            return opcion
