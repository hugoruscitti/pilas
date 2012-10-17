# -*- encoding: utf-8 -*-
import pilas
from pilas.actores.globo import Globo


class GloboElegir(Globo):

    def __init__(self, texto, opciones, funcion_a_invocar, x=0, y=0, dialogo=None):
        self.dialogo = dialogo
        self.opciones = opciones
        self.funcion_a_invocar = funcion_a_invocar

        self.lista_seleccion = pilas.interfaz.ListaSeleccion(opciones, self._cuando_selecciona_opcion, x, y)
        self.lista_seleccion.escala = 0.1
        self.lista_seleccion.escala = [1], 0.2
        self.lista_seleccion.z = 1

        Globo.__init__(self, texto, x, y, dialogo=dialogo, 
                       ancho_globo=self.lista_seleccion.ancho_opciones+24,
                       alto_globo=self.lista_seleccion.alto_opciones + (self.lista_seleccion.separacion_entre_opciones * len(self.opciones) * 2))
        self.z = 2

    def colocar_origen_del_globo(self, x, y):
        Globo.colocar_origen_del_globo(self, x, y)
        
        self.lista_seleccion.centro = ("derecha", "abajo")
        self.lista_seleccion.x = x - (self.ancho_globo - self.lista_seleccion.ancho_opciones) + 12 
        self.lista_seleccion.y = y + 35

    def _obtener_area_para_el_texto(self, texto):
        ancho, alto = self.lienzo.obtener_area_de_texto(texto, tamano=14)
        opciones_ancho, opciones_alto = self.lienzo.obtener_area_para_lista_de_texto(self.opciones, tamano=14)     
        return ancho + opciones_ancho, alto + opciones_alto 
        
    def _escribir_texto(self, texto):
        self.lienzo.escribir(texto, 12, 25, tamano=14)

    def cuando_quieren_avanzar(self, *k):
        pass

    def _cuando_selecciona_opcion(self, opcion):
        self.funcion_a_invocar(opcion)
        Globo.cuando_quieren_avanzar(self)
        self.lista_seleccion.eliminar()
