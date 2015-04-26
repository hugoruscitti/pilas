# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilasengine
from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento

VELOCIDAD = 10

NORTE = 0
SUR = 2
ESTE = 1
OESTE = 3


class Maton(Actor):
    """Representa un personaje de juego tipo RPG."""

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar_grilla("rpg/maton.png", 3, 4)

        self.direccion = SUR
        self.hacer(Esperando)
        self.velocidad = VELOCIDAD
        self.figura = self.pilas.fisica.Circulo(0, 0, 5)
        self.figura.escala_de_gravedad = 0
        self.figura.sin_rotacion = True

    def definir_cuadro(self, indice):
        self.imagen.definir_cuadro(indice)
        self.definir_centro((17, 48))

    def actualizar(self):
        self.x = self.figura.x
        self.y = self.figura.y

class Esperando(Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor

        if receptor.direccion == NORTE:
            receptor.definir_cuadro(1)
        elif receptor.direccion == ESTE:
            receptor.definir_cuadro(4)
        elif receptor.direccion == SUR:
            receptor.definir_cuadro(7)
        elif receptor.direccion == OESTE:
            receptor.definir_cuadro(10)

    def actualizar(self):
        self.receptor.figura.velocidad_x = 0
        self.receptor.figura.velocidad_y = 0

        if self.pilas.control.izquierda:
            self.receptor.hacer(Caminando)
            return True
        elif self.pilas.control.derecha:
            self.receptor.hacer(Caminando)
            return True
        elif self.pilas.control.arriba:
            self.receptor.hacer(Caminando)
            return True
        elif self.pilas.control.abajo:
            self.receptor.hacer(Caminando)
            return True

class Caminando(Esperando):

    def iniciar(self, receptor):
        self.receptor = receptor
        self._repeticion_cuadro = 3
        self.paso = 0
        self.cuadros = [[1,1,1,1,0,0,0,0,1,1,1,1,2,2,2,2],
                        [4,4,4,4,3,3,3,3,4,4,4,4,5,5,5,5],
                        [7,7,7,7,6,6,6,6,7,7,7,7,8,8,8,8],
                        [10,10,10,10,9,9,9,9,10,10,10,10,11,11,11,11]]

    def actualizar(self):
        self.avanzar_animacion()

        dx = 0
        dy = 0

        if self.pilas.control.izquierda:
            dx = self.receptor.velocidad * -1
            self.receptor.direccion = OESTE
        elif self.pilas.control.derecha:
            dx = self.receptor.velocidad
            self.receptor.direccion = ESTE
        elif self.pilas.control.arriba:
            dy = self.receptor.velocidad
            self.receptor.direccion = NORTE
        elif self.pilas.control.abajo:
            dy = self.receptor.velocidad * -1
            self.receptor.direccion = SUR
        else:
            self.receptor.hacer(Esperando)
            return True

        self.receptor.figura.velocidad_x = dx
        self.receptor.figura.velocidad_y = dy

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros[self.receptor.direccion]):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.receptor.direccion][self.paso])
