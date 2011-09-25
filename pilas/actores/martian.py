# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
from pilas.comportamientos import Comportamiento

VELOCIDAD = 100


class Martian(Actor):

    def __init__(self, x=0, y=0):
        Actor.__init__(self, x=x, y=y)
        self.imagen = pilas.imagenes.cargar_grilla("marcianitos/martian.png", 12)
        self.definir_cuadro(0)
        self.figura = pilas.fisica.Circulo(0, 0, 18, friccion=0, amortiguacion=0, restitucion=0.1)
        self.hacer(Esperando())

    def definir_cuadro(self, indice):
        self.imagen.definir_cuadro(indice)
        self.definir_centro((32, 123))

    def actualizar(self):
        "Sigue el movimiento de la figura."
        self.x = self.figura.x
        self.y = self.figura.y - 15
        self.figura.rotacion = 0

    def crear_disparo(self):
        if self.espejado:
            rotacion = -90
        else:
            rotacion = 90

        disparo = pilas.actores.Disparo(x=self.x, y=self.y+20, rotacion=rotacion, velocidad=10)

    def puede_saltar(self):
        dx, dy = self.figura.obtener_velocidad_lineal()
        return -2 < dy < 2

class Esperando(Comportamiento):
    "Un actor en posicion normal o esperando a que el usuario pulse alguna tecla."

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(0)

    def actualizar(self):

        if pilas.mundo.control.izquierda:
            self.receptor.hacer(Caminando())
        elif pilas.mundo.control.derecha:
            self.receptor.hacer(Caminando())

        if pilas.mundo.control.arriba and self.receptor.puede_saltar():
            self.receptor.hacer(Saltando())

        if pilas.mundo.control.boton:
            self.receptor.hacer(Disparar(self.receptor))

class Caminando(Comportamiento):

    def __init__(self):
        self.cuadros = [1, 1, 1, 2, 2, 2]
        self.paso = 0

    def iniciar(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        self.avanzar_animacion()

        if pilas.mundo.control.izquierda:
            self.receptor.figura.definir_velocidad_lineal(-VELOCIDAD)
            self.receptor.espejado = True
        elif pilas.mundo.control.derecha:
            self.receptor.figura.definir_velocidad_lineal(+VELOCIDAD)
            self.receptor.espejado = False
        else:
            self.receptor.figura.definir_velocidad_lineal(0)
            self.receptor.hacer(Esperando())

        if pilas.mundo.control.arriba:
            self.receptor.hacer(Saltando())

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.paso])

class Saltando(Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(3)
        self.esta_bajando = False
        self.receptor.figura.definir_velocidad_lineal(None, 300)


    def actualizar(self):

        # obtiene la velocidad del personaje para detectar cuando
        # toca el suelo.
        vx, vy = self.receptor.figura.obtener_velocidad_lineal()

        if vy < 0:
            self.esta_bajando = True

        if self.esta_bajando and -2 < vy < 2:
            self.receptor.figura.definir_velocidad_lineal(0,0)
            self.receptor.hacer(Esperando())

        if pilas.mundo.control.izquierda:
            self.receptor.espejado = True
            self.receptor.figura.definir_velocidad_lineal(-VELOCIDAD)
        elif pilas.mundo.control.derecha:
            self.receptor.espejado = False
            self.receptor.figura.definir_velocidad_lineal(VELOCIDAD)
        else:
            self.receptor.figura.definir_velocidad_lineal(0)

class Disparar(Comportamiento):

    def __init__(self, receptor):
        self.cuadros = [6, 6, 7, 7, 8, 8]
        self.paso = 0
        receptor.crear_disparo()

    def actualizar(self):
        termina = self.avanzar_animacion()

        if termina:
            self.receptor.hacer(Esperando())

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0
            return True

        self.receptor.definir_cuadro(self.cuadros[self.paso])
