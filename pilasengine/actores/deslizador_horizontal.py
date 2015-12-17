# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor
from pilasengine import colores

ALTURA = 15

class DeslizadorHorizontal(Actor):

    def pre_iniciar(self, x=0, y=0, actor='actor', propiedad='x', _min=0, _max=100):
        pass
        
    def iniciar(self,  x=0, y=0, _min=0, _max=100, etiqueta="sin titulo", valor_inicial=-21):
        self.min = _min
        self.max = _max
        self.x = x
        self.y = y
        self.rango = _max - _min
        self.texto_etiqueta = etiqueta
        self.imagen = self.pilas.imagenes.cargar_superficie(100, ALTURA)
        self.progreso = valor_inicial

        self.progreso_sobre_100 = ((valor_inicial - _min) / float(self.rango))*100
        self.actualizar_imagen()

        self.figura_de_colision = None
        ancho, alto = 100, ALTURA
        self.radio_de_colision = None
        self.click = False
        self.funciones = []

        self.etiqueta = self.pilas.actores.Texto(self.texto_etiqueta, magnitud=10, y=-alto/2)
        self.etiqueta.derecha = -10
        self.contador = self.pilas.actores.Texto("0", magnitud=10, x=ancho + 15, y=-alto/2)

        self.etiqueta.figura_de_colision = None
        self.contador.figura_de_colision = None

        self.agregar(self.etiqueta)
        self.agregar(self.contador)

        self.pilas.escena.click_de_mouse.conectar(self.click_del_mouse)
        self.pilas.escena.mueve_mouse.conectar(self.movimiento_del_mouse)
        self.pilas.escena.termina_click.conectar(self.termino_del_click)

        self.actualizar_texto()

    def actualizar_imagen(self):
        self.imagen.limpiar()
        self.imagen.rectangulo(0, 0, int(self.progreso_sobre_100), self.alto, color=colores.blanco, relleno=True)
        self.imagen.rectangulo(1, 1, self.ancho-2, self.alto-2, color=colores.negro, relleno=False, grosor=2)

    def click_del_mouse(self, click):
        if self.colisiona_con_un_punto(click.x, click.y):
            self.click = True
            self.movimiento_del_mouse(click)

    def movimiento_del_mouse(self, movimiento):
        if self.click:
            pos_x = movimiento.x - self.izquierda
            pos_x = max(pos_x, 0)
            pos_x = min(pos_x, self.ancho)
            self.progreso_sobre_100 = pos_x

            self.progreso = ((pos_x / float(self.ancho)) * self.rango) + self.min

            self.actualizar_texto()

            self.ejecutar_funciones(self.progreso)
            self.actualizar_imagen()

    def termino_del_click(self, noclick):
        self.click = False

    def conectar(self, f):
        self.funciones.append(f)

    def desconectar(self, f):
        self.funciones.remove(f)

    def ejecutar_funciones(self, valor):
        for i in self.funciones:
            i(valor)

    def actualizar_texto(self):
        if self.progreso > 0:
            self.contador.texto = str(self.progreso)[:4]
        else:
            self.contador.texto = str(self.progreso)[:5]
