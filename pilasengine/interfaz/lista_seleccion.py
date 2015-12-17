# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.interfaz import elemento
from pilasengine import colores

class ListaSeleccion(elemento.Elemento):

    def __init__(self, pilas=None, opciones=['primer opcion'], funcion_a_ejecutar=None, x=0, y=0):
        super(ListaSeleccion, self).__init__(pilas, x=x, y=y)
        self.opciones = opciones
        self.funcion_a_ejecutar = funcion_a_ejecutar
        self.opcion_seleccionada = None

        ancho, _ = self.pilas.utils.obtener_area_de_texto("\n".join(opciones))

        self.alto_opcion = self.pilas.utils.obtener_area_de_texto("texto")[1]
        self.alto_opciones = self.alto_opcion * len(self.opciones)
        self.ancho_opciones = ancho
        self.separacion_entre_opciones = 2  # en pixels

        self.imagen = self.pilas.imagenes.cargar_superficie(int(ancho + 35), int(self.alto_opciones + (self.separacion_entre_opciones * len(self.opciones) * 2)))

        self._pintar_opciones()

        self.pilas.eventos.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        self.pilas.eventos.click_de_mouse.conectar(self.cuando_hace_click_con_el_mouse)

        self.centro = ("centro", "centro")
        self.fijo = True

    def _pintar_opciones(self, opcion_debajo_del_cursor=None):
        self.imagen.pintar(self.pilas.colores.blanco)

        if self.opcion_seleccionada != None:
            self.imagen.rectangulo(0, self.opcion_seleccionada * (self.alto_opcion + (self.separacion_entre_opciones * 2)), self.imagen.ancho(), self.alto_opcion + (self.separacion_entre_opciones * 2), relleno=True, color=colores.naranja)

        if opcion_debajo_del_cursor != None:
            self.imagen.rectangulo(0, opcion_debajo_del_cursor * (self.alto_opcion + (self.separacion_entre_opciones * 2)), self.imagen.ancho(), self.alto_opcion + (self.separacion_entre_opciones * 2), relleno=True, color=colores.naranja_transparente)

        for indice, opcion in enumerate(self.opciones):
            self.imagen.texto(opcion, 15, y=self.alto_opcion * indice + 1 +(self.separacion_entre_opciones * 2 * indice), color=colores.negro)

    def cuando_mueve_el_mouse(self, evento):
        if (self.activo):
            if self.colisiona_con_un_punto(evento.x, evento.y):
                opcion_debajo_del_cursor = self._detectar_opcion_bajo_el_mouse(evento)
                self._pintar_opciones(opcion_debajo_del_cursor)
            else:
                self._pintar_opciones(None)

    def cuando_hace_click_con_el_mouse(self, evento):
        if (self.activo):
            if self.colisiona_con_un_punto(evento.x, evento.y):
                opcion_debajo_del_cursor = self._detectar_opcion_bajo_el_mouse(evento)
                self.opcion_seleccionada = opcion_debajo_del_cursor
                self._pintar_opciones(opcion_debajo_del_cursor)

                if self.funcion_a_ejecutar:
                    self.funcion_a_ejecutar(self.opciones[opcion_debajo_del_cursor])
                else:
                    print "Cuidado, no has definido funcion a ejecutar en la lista de seleccion."

    def _detectar_opcion_bajo_el_mouse(self, evento):
        opcion = int((self.arriba - evento.y ) / (self.alto_opcion + (self.separacion_entre_opciones * 2)))
        if opcion in range(0, len(self.opciones)):
            return opcion