# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor


class Tortuga(Actor):
    """Representa una tortuga que se puede mover por la pantalla.

    Este actor está profundamente inspirado por la tortuga de Logo, creada
    por Seymour Papert en el año 1967.
    """

    def __init__(self, x=0, y=0, dibuja=True):
        """Inicializa la tortuga.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param dibuja: Indica si a tortuga dejará marcada una linea al moverse.
        """
        self.pizarra = pilas.actores.Pizarra()

        imagen = pilas.imagenes.cargar('tortuga.png')
        Actor.__init__(self, imagen, x=x, y=y)

        self.rotacion = 0
        self.velocidad = 6

        self.anterior_x = x
        self.anterior_y = y

        if dibuja:
            self.bajalapiz()
        else:
            self.subelapiz()

        self.color = pilas.colores.negro

    def avanzar(self, pasos):
        """Se mueve hacia adelante la cantidad de pasos indicada.

        :param pasos: Los pasos que debe avanzar.
        """
        self.hacer_luego(pilas.comportamientos.Avanzar(pasos, self.velocidad))

    def giraderecha(self, delta):
        """Da un giro hacia la derecha de la tortuga.

        :param delta: Los grados que digará en ese sentido.
        """
        self.hacer_luego(pilas.comportamientos.Girar(abs(delta), self.velocidad))

    def giraizquierda(self, delta):
        """Realiza un giro hacia la izquierda.

        :param delta: Los grados que digará en ese sentido.
        """
        self.hacer_luego(pilas.comportamientos.Girar(-abs(delta), self.velocidad))

    def actualizar(self):
        """Actualiza su estado interno."""
        if self.anterior_x != self.x or self.anterior_y != self.y:
            if self.lapiz_bajo:
                self.dibujar_linea_desde_el_punto_anterior()
            self.anterior_x = self.x
            self.anterior_y = self.y

    def dibujar_linea_desde_el_punto_anterior(self):
        """Realiza el trazado de una linea desde su posición actual hacia la anterior."""
        self.pizarra.linea(self.anterior_x, self.anterior_y, self.x, self.y, self.color, grosor=4)

    def bajalapiz(self):
        """Le indica a la tortuga si debe comenzar a dibujar con cada movimiento."""
        self.lapiz_bajo = True

    def subelapiz(self):
        """Le indica a la tortuga que deje de dibujar con cada movimiento."""
        self.lapiz_bajo = False

    def pon_color(self, color):
        """Define el color de trazado cuando comienza a moverse."""
        self.color = color

    def crear_poligono(self, lados=4, escala=100, sentido=-1):
        """dibuja un poligono de lados de los lados indicados.

        :param lados: La cantidad de lados a dibujar.
        :param escala: El tamaño del polígono a dibujar.
        :param sentido: El sentido de dibujado, -1 indica hacia la izquierda y 1 hacia la derecha.
        """

        for i in range(lados):
            rotacion = 360 / lados
            self.avanzar(escala)
            if sentido == 1:
                self.giraderecha(rotacion)
            else:
                self.giraizquierda(rotacion)

    def crear_circulo(self, radio=30, sentido=-1):
        """Dibuja un circulo.

        :param radio: El radio que deberá tener el circulo.
        :param sentido: El sentido de dibujado, -1 indica hacia la izquierda y 1 hacia la derecha.
        """
        for i in range(36):
            self.avanzar(radio)
            if sentido == 1:
                self.giraderecha(10)
            else:
                self.giraizquierda(10)

    # Alias de metodos
    av = avanzar
    gd = giraderecha
    gi = giraizquierda
    bl = bajalapiz
    sl = subelapiz
    pc = pon_color

    def get_color(self):
        """Retorna el color que se utilizará para trazar."""
        return self._color

    def set_color(self, color):
        """Define el color que se utilizará para trazar.

        :param color: El color a utilizar.
        """
        self._color = color

    color = property(get_color, set_color)

    def pintar(self, color=None):
        """Pinta todo el fondo de un solo color.

        :param color: El color que se utilizará para pintar el fondo.
        """
        self.pizarra.pintar(color)
