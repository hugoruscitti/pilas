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
from pilas.actores import Actor


class Deslizador(Actor):

    def __init__(self, x=0, y=0, ruta_barra = 'interfaz/barra.png',
                                 ruta_deslizador = 'interfaz/deslizador.png'):

        self.deslizador = None
        Actor.__init__(self, ruta_barra, x=x, y=y)
        self.deslizador = Actor(ruta_deslizador, self.x, self.y)
        self.centro = ('izquierda', 'centro')
        
        self.click = False
        
        pilas.eventos.click_de_mouse.conectar(self.click_del_mouse)
        pilas.eventos.mueve_mouse.conectar(self.movimiento_del_mouse)
        pilas.eventos.termina_click.conectar(self.termino_del_click)

        self.progreso = 0
        self.posicion_relativa_x = 0

        self.funciones = []

        # establecemos posicion inicial
        self.x = x
        self.y = y

    def set_transparencia(self, nuevo_valor):
        self.transparencia = nuevo_valor
        self.deslizador.transparencia = nuevo_valor

    def definir_posicion(self, x, y):
        self.limite_izq = self.x
        self.limite_der = self.x + self.obtener_ancho()

        self._actor.definir_posicion(x, y)
        if self.deslizador:
            self.deslizador.definir_posicion(x + self.posicion_relativa_x, y)

    def conectar(self, f):
        self.funciones.append(f)        

    def desconectar(self, f):
        self.funciones.remove(f)

    def ejecutar_funciones(self, valor):
        for i in self.funciones:
            i(valor)
    
    def click_del_mouse(self, click):
 
        if self.deslizador.colisiona_con_un_punto(click.x, click.y):
            self.click = True

    def movimiento_del_mouse(self, movimiento):
        if self.click == True:
            ancho = self.obtener_ancho()
            factor = (self.deslizador.x + (ancho - abs(self.x))) / ancho - 1
            self.progreso = factor
            
            self.ejecutar_funciones(factor)

            self.deslizador.x = movimiento.x

            if self.deslizador.x <= self.limite_izq:
                self.deslizador.x = self.limite_izq

            elif self.deslizador.x >= self.limite_der:
                self.deslizador.x = self.limite_der

            self.posicion_relativa_x = self.deslizador.x - self.x
                

    def termino_del_click(self, noclick):
        self.click = False
