# -*- encoding: utf-8 -*-
import pilas
from pilas.actores.globo import Globo

class GloboElegir(Globo):
    
    def __init__(self, texto, opciones, funcion_a_invocar, x=0, y=0, dialogo=None):
        self.dialogo = dialogo
        self.opciones = opciones
        self.funcion_a_invocar = funcion_a_invocar
        Globo.__init__(self, texto, x, y, dialogo=dialogo)
    
        self.lista_seleccion = pilas.interfaz.ListaSeleccion(opciones, self._cuando_selecciona_opcion, x, y)
        self._actualizar_posicion_de_la_lista_de_seleccion()
        
    def colocar_origen_del_globo(self, x, y):
        Globo.colocar_origen_del_globo(self, x, y)
        self._actualizar_posicion_de_la_lista_de_seleccion()

    def _actualizar_posicion_de_la_lista_de_seleccion(self):
        self.lista_seleccion.izquierda = self.izquierda + 10
        self.lista_seleccion.abajo = self.abajo + 33
        self.lista_seleccion.centro = ("centro", "centro")

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
