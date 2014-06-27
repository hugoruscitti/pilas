# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.interfaz import elemento

class Deslizador(elemento.Elemento):

    def __init__(self, pilas=None, x=0, y=0, ruta_barra = 'interfaz/barra.png',
                                 ruta_deslizador = 'interfaz/deslizador.png'):
        """Inicializa al actor.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param ruta_barra: Imagen que se usará como barra.
        :param ruta_deslizador: Imagen para presentar al manejado o cursor del deslizador.
        """
        self.deslizador = None
        elemento.Elemento.__init__(self, pilas, x=x, y=y)
        self.imagen = ruta_barra
        self.deslizador = self.pilas.actores.Actor(self.x, self.y)
        self.deslizador.imagen = ruta_deslizador
        self.deslizador.fijo = True
        self.deslizador.z = self.z - 10
        self.centro = ('izquierda', 'centro')

        self.click = False

        self.pilas.escena.click_de_mouse.conectar(self.click_del_mouse)
        self.pilas.escena.mueve_mouse.conectar(self.movimiento_del_mouse)
        self.pilas.escena.termina_click.conectar(self.termino_del_click)

        self.progreso = 0
        self.posicion_relativa_x = 0

        self.funciones = []

        # establecemos posicion inicial
        self.x = x
        self.y = y
        self.fijo = True
        self.definir_posicion(x, y)

    def set_transparencia(self, nuevo_valor):
        """Define la transparecia del actor."""
        self.transparencia = nuevo_valor
        self.deslizador.transparencia = nuevo_valor

    def definir_posicion(self, x, y):
        """Cambia la posición.

        :param x: Nueva posición horizontal.
        :param y: Nueva posición vertical.
        """
        self.limite_izq = self.x
        self.limite_der = self.x + self.obtener_ancho()

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
        if (self.activo):
            if self.deslizador.colisiona_con_un_punto(click.x, click.y):
                self.click = True

    def movimiento_del_mouse(self, movimiento):
        if (self.activo):
            if self.click == True:
                ancho = self.obtener_ancho()
                deslizador_pos_x = self.deslizador.x - self.x
                factor = (deslizador_pos_x + ancho) / ancho - 1
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

    def mostrar(self):
        elemento.Elemento.mostrar(self)
        self.deslizador.transparencia = 0

    def ocultar(self):
        elemento.Elemento.ocultar(self)
        self.deslizador.transparencia = 100

    def eliminar(self):
        self.deslizador.eliminar()
        elemento.Elemento.eliminar(self)