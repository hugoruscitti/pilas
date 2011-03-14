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

VELOCIDAD = 10000


class Martian(Actor):

    def __init__(self, x=0, y=0):
        Actor.__init__(self, x=x, y=y)
        self.animacion = pilas.imagenes.cargar_grilla("marcianitos/martian.png", 12)
        self.definir_cuadro(0)
        self.hacer(Esperando())
        self.figura = pilas.fisica.Rectangulo(0, 0, 10, 10, restitucion=0.00001, friccion=0.00)

        #self.aprender(pilas.habilidades.PisaPlataformas)

    def definir_cuadro(self, indice):
        self.animacion.definir_cuadro(indice)
        self.animacion.asignar(self)
        self.definir_centro((32, 123))

    def mover(self, x, y):
        if x > 1:
            self.espejado = False

        if x < -1:
            self.espejado = True

        self.figura.impulsar(x, y)

    def actualizar(self):
        "Sigue el movimiento de la figura."
        self.x = self.figura.x
        self.y = self.figura.y
        vx, vy = self.figura.obtener_velocidad_lineal()
        self.figura.definir_velocidad_lineal(0, vy)
        self.figura.definir_rotacion(0)

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

        if pilas.mundo.control.arriba:
            self.receptor.hacer(Saltando())


class Caminando(Comportamiento):

    def __init__(self):
        self.cuadros = [1, 1, 1, 2, 2, 2]
        self.paso = 0

    def actualizar(self):
        vx, vy = self.receptor.figura.obtener_velocidad_lineal()
        print vy
        self.avanzar_animacion()

        if pilas.mundo.control.izquierda:
            self.receptor.mover(-VELOCIDAD, 0)
        elif pilas.mundo.control.derecha:
            self.receptor.mover(VELOCIDAD, 0)
        else:
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
        self.receptor.mover(0, -600000)

        vx, vy = self.receptor.figura.obtener_velocidad_lineal()

        if vy > 0:
            self.esta_subiendo = False
        else:
            self.esta_subiendo = True

    def actualizar(self):

        # obtiene la velocidad del personaje para detectar cuando
        # toca el suelo.
        vx, vy = self.receptor.figura.obtener_velocidad_lineal()

        if self.esta_subiendo:
            if vy < 0:
                self.esta_subiendo = False
        else:
            # Esta bajando...
            if vy > 0:
                #print "Hey, esta rebotando..."
                self.receptor.figura.definir_velocidad_lineal(0,0)
                self.receptor.hacer(Esperando())

        #self.receptor.y += self.dy
        #self.dy -= 0.3

        #if self.receptor.y < 0:
        #    self.receptor.y = 0
        #    self.receptor.hacer(Esperando())

        if pilas.mundo.control.izquierda:
            self.receptor.espejado = True
            self.receptor.mover(-VELOCIDAD, 0)
        elif pilas.mundo.control.derecha:
            self.receptor.espejado = False
            self.receptor.mover(+VELOCIDAD, 0)
