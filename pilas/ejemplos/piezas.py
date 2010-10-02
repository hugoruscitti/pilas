# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
import random


class Piezas(pilas.escenas.Normal):
    """Representa la escena de rompecabezas.

    La escena comienza con una imagen que se descompone en muchos
    actores Pieza.
    """

    def __init__(self, ruta_a_la_imagen="ejemplos/data/piezas.png", filas=6, columnas=6):
        #filas=4, columnas=7):
        pilas.actores.eliminar_a_todos()
        pilas.escenas.Normal.__init__(self, pilas.colores.gris_oscuro)
        grilla = pilas.imagenes.Grilla(ruta_a_la_imagen, columnas, filas)
        self.crear_piezas(grilla, filas, columnas)
        self.pieza_en_movimiento = None

        pilas.eventos.click_de_mouse.conectar(self.al_hacer_click)
        pilas.eventos.termina_click.connect(self.al_soltar_el_click)
        pilas.eventos.mueve_mouse.connect(self.al_mover_el_mouse)

    def crear_piezas(self, grilla, filas, columnas):
        "Genera todas las piezas en base al tamaño del constructor."
        self.piezas = []
        self.grupos = {}

        i = 0

        for x in range(filas * columnas):
            pieza = Pieza(self, grilla, x, filas, columnas)
            pieza.x = random.randint(-200, 200)
            pieza.y = random.randint(-200, 200)
            self.grupos[x] = [x]

            self.piezas.append(pieza)
            i += 1

            if i == 2:
                break

    def al_hacer_click(self, **kv):
        "Atiente cualquier click que realice el usuario en la pantalla."
        pieza_debajo_de_mouse = pilas.actores.obtener_actor_en(kv['x'], kv['y'])

        if pieza_debajo_de_mouse:
            self.pieza_en_movimiento = pieza_debajo_de_mouse

    def al_soltar_el_click(self, **kv):
        if self.pieza_en_movimiento:
            self.pieza_en_movimiento.soltar()
            self.pieza_en_movimiento = None

    def al_mover_el_mouse(self, **kv):
        if self.pieza_en_movimiento:
            self.pieza_en_movimiento.mover(kv['dx'], kv['dy'])
            

class Pieza(pilas.actores.Animado):
    """Representa una pieza del rompecabezas.

    Esta pieza se puede arrastrar con el mouse y cuando se suelta
    intentará conectarse con las demás."""

    def __init__(self, escena_padre, grilla, cuadro, filas, columnas):
        pilas.actores.Animado.__init__(self, grilla)

        self.numero = cuadro

        self.asignar_numero_de_piezas_laterales(cuadro, columnas)

        self.definir_cuadro(cuadro)

        self.radio_de_colision = self.obtener_ancho() / 2 + 10
        self.escena_padre = escena_padre
        self.piezas_conectadas = []

    def asignar_numero_de_piezas_laterales(self, cuadro, columnas):
        "Guarda el numero de las piezas que se pueden conectar en sus bordes."
        self.numero_arriba = cuadro - columnas
        self.numero_abajo = cuadro + columnas

        if cuadro % columnas == 0:
            self.numero_izquierda = -1
        else:
            self.numero_izquierda = cuadro - 1

        if cuadro % columnas == columnas -1:
            self.numero_derecha = -1
        else:
            self.numero_derecha = cuadro + 1


    def soltar(self):
        # Busca todas las colisiones entre esta pieza
        # que se suelta y todas las demás.
        colisiones = pilas.colisiones.obtener_colisiones(self, self.escena_padre.piezas)

        for x in colisiones:
            self.intentar_conectarse_a(x)




    def intentar_conectarse_a(self, otra):
        "Intenta vincular dos piezas, siempre y cuando coincidan en sus bordes."

        # Intenta conectarse a la derecha.
        if self.numero_derecha == otra.numero:    # es la pieza derecha, trato de conectarla.
            print "Se ha posado a izquerda de la pieza que corresponde"
            if pilas.utils.distancia(self.derecha, otra.izquierda) < 12:
                otra.izquierda = self.derecha
                otra.arriba = self.arriba

                self.conectar_con(otra)
                otra.conectar_con(self)
        elif self.numero_izquierda == otra.numero:
            if pilas.utils.distancia(self.izquierda, otra.derecha) < 12:
                otra.derecha = self.izquierda
                otra.arriba = self.arriba

                self.conectar_con(otra)
                otra.conectar_con(self)

        print "Conectando a ", otra

    def conectar_con(self, otra_pieza):
        if otra_pieza not in self.piezas_conectadas:
            self.piezas_conectadas.append(otra_pieza)

            #for x in otra_pieza.piezas_conectadas:
            #    if x not in self.piezas_conectadas:
            #        self.piezas_conectadas.append(x)

    def mover(self, dx, dy):
        "Arrastra el actor a la posicion indicada por el puntero del mouse."
        self.x += dx
        self.y += dy
        self.mover_las_piezas_conectadas(dx, dy)

    def mover_las_piezas_conectadas(self, dx, dy):
        for pieza in self.piezas_conectadas:
            pieza.x += dx
            pieza.y += dy

    def __repr__(self):
        return "<<Pieza %d>>" %(self.animacion.obtener_cuadro())
