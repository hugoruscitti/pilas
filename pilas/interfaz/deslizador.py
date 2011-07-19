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

        Actor.__init__(self, ruta_barra, x=x, y=y)
        self.centro = ('izquierda', 'centro')
        self.deslizador = Actor(ruta_deslizador, self.x, self.y)
        
        self.click = False
        
        pilas.eventos.click_de_mouse.conectar(self.click_del_mouse)
        pilas.eventos.mueve_mouse.conectar(self.movimiento_del_mouse)
        pilas.eventos.termina_click.conectar(self.termino_del_click)

        self.progreso = 0

        self.funciones = []

        # establecemos posicion inicial
        self.x = x
        self.y = y

        self.deslizador.x = x
        self.deslizador.y = y
        
        self.a = self.obtener_ancho() 
        
        self.limite_izq = self.x
        self.limite_der = self.x + self.a


    def set_transparencia(self, nuevo_valor):
        self.transparencia = nuevo_valor
        self.deslizador.transparencia = nuevo_valor

    def set_x(self, x):
        self.x = x
        self.limite_izq = self.x
        self.limite_der = self.x + self.a
        self.deslizador.x = x

    def set_y(self, y):
        self.y = y
        self.deslizador.y = y
        
          
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
            factor = (self.deslizador.x + (self.a - self.x)) / self.a - 1
            self.progreso = factor
            self.ejecutar_funciones(factor)

            self.deslizador.x = movimiento.x
            if self.deslizador.x <= self.limite_izq:
                self.deslizador.x = self.limite_izq

            elif self.deslizador.x >= self.limite_der:
                self.deslizador.x = self.limite_der
                

    def termino_del_click(self, noclick):
        self.click = False
