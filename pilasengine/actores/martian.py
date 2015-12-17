# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento
import pilasengine

class Martian(Actor):
    """Es un personaje de un marciano que puede caminar y saltar.

        .. image:: ../../pilas/data/manual/imagenes/actores/martian.png

    Este actor se puede mover con el teclado, pulsando las teclas ``izquierda``,
    ``arriba``, ``abajo`` y ``derecha``.

    El marciano necesita un mapa para no caer al vacio y desaparecer de la
    pantalla.

        >>> marciano = pilas.actores.Martian(pilas.actores.Mapa())

    """

    def pre_iniciar(self, mapa=None, x=0, y=0):
        self.x = x
        self.y = y
        self.mapa = mapa
        self.imagen = self.pilas.imagenes.cargar_grilla("marcianitos/martian.png", 12)
        self.definir_cuadro(0)
        self.hacer(Esperando)

        self.velocidad = 3

        self.colisiona_arriba_izquierda = False
        self.colisiona_arriba_derecha = False
        self.colisiona_abajo_izquierda = False
        self.colisiona_abajo_derecha = False

        self.obtener_colisiones()

        if not mapa:
            self.definir_figura_fisica()

    def definir_figura_fisica(self):
        self.figura_del_actor = self.pilas.fisica.Rectangulo(0, 0, 20, 50)
        self.figura_del_actor.sin_rotacion = True

    def definir_cuadro(self, indice):
        """Define el cuadro de animación a mostrar.

        :param indice: El número de cuadro comenzando desde 0.
        """
        self.imagen.definir_cuadro(indice)
        self.definir_centro((32, 68))

    def actualizar(self):
        "Sigue el movimiento de la figura."
        if self.mapa:
            return
        else:
            self.x = self.figura_del_actor.x
            self.y = self.figura_del_actor.y - 25

    def puede_saltar(self):
        "Indica si el persona puede saltar."
        return True

    def obtener_distancia_al_suelo(self):
        "Retorna la distancia en pixels al suelo."
        if not self.mapa:
            return 0
        else:
            return self.mapa.obtener_distancia_al_suelo(self.x, self.y, 100)

    def obtener_colisiones(self):
        if self.mapa:
            self.colisiona_arriba_izquierda = self.mapa.es_punto_solido(self.izquierda, self.arriba)
            self.colisiona_arriba_derecha = self.mapa.es_punto_solido(self.derecha, self.arriba)
            self.colisiona_abajo_izquierda = self.mapa.es_punto_solido(self.izquierda, self.abajo)
            self.colisiona_abajo_derecha = self.mapa.es_punto_solido(self.derecha, self.abajo)
        else:
            self.colisiona_arriba_izquierda = False
            self.colisiona_arriba_derecha = False
            self.colisiona_abajo_izquierda = False
            self.colisiona_abajo_derecha = False

    def mover(self, vx):
        if vx > 0:
            self.espejado = False
            self.obtener_colisiones()

            if not(self.colisiona_arriba_derecha or self.colisiona_abajo_derecha):
                self.x += vx
        elif vx < 0:
            self.espejado = True
            self.obtener_colisiones()

            if not(self.colisiona_arriba_izquierda or self.colisiona_abajo_izquierda):
                self.x += vx

        if not self.mapa:
            self.figura_del_actor.velocidad_x = vx



class Esperando(Comportamiento):
    """Representa al actor en posicion normal.

    Este comportamiento espera a que el usuario pulse
    alguna tecla para entrar en movimiento.
    """

    def iniciar(self, receptor):
        """Inicia el comportamiento y define los valores iniciales.

        :param receptor: El actor que será controlado por este comportamiento."
        """
        self.receptor = receptor
        self.receptor.definir_cuadro(0)
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        if self.control.izquierda:
            self.receptor.hacer(Caminando)
        elif self.control.derecha:
            self.receptor.hacer(Caminando)

        if self.control.arriba and self.receptor.puede_saltar():
            self.receptor.hacer(Saltando, -8)

        self.caer_si_no_toca_el_suelo()

    def caer_si_no_toca_el_suelo(self):
        if self.receptor.obtener_distancia_al_suelo() > 0:
            self.receptor.hacer(Saltando, 0)

class Caminando(Esperando):
    """Representa al actor caminando hacia la izquierda o derecha."""

    def iniciar(self, receptor):
        """Inicia el comportamiento y define los valores iniciales.

        :param receptor: El actor que será controlado por este comportamiento."
        """
        self.cuadros = [1, 1, 1, 2, 2, 2]
        self.paso = 0
        self.receptor = receptor
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        self.avanzar_animacion()

        vx = 0

        if self.control.izquierda:
            vx = -(self.receptor.velocidad)
            self.receptor.mover(vx)

        elif self.control.derecha:
            vx = self.receptor.velocidad
            self.receptor.mover(vx)
        else:
            self.receptor.hacer(Esperando)

        if self.control.arriba:
            self.receptor.hacer(Saltando, -8)

        self.caer_si_no_toca_el_suelo()

    def avanzar_animacion(self):
        """Cambia el cuado de animación para avanzar la animación"""
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.paso])

class Saltando(Comportamiento):
    """Representa al actor realizando un salto."""

    def iniciar(self, receptor, velocidad_de_salto):
        """Inicia el comportamiento y define los valores iniciales.

        :param receptor: El actor que será controlado por este comportamiento."
        """
        self.velocidad_de_salto = velocidad_de_salto
        self.receptor = receptor
        self.receptor.definir_cuadro(3)
        self.control = receptor.pilas.escena_actual().control

    def actualizar(self):
        self.velocidad_de_salto += 0.25
        distancia = self.receptor.obtener_distancia_al_suelo()

        if not self.receptor.mapa:
            self.receptor.figura_del_actor.velocidad_y = -self.velocidad_de_salto

        # Si toca el suelo se detiene.
        if self.velocidad_de_salto > distancia:
            self.receptor.y -= distancia
            self.receptor.hacer(Esperando)
        else:
            self.receptor.y -= self.velocidad_de_salto

        # obtiene la veloridad del personaje para detectar cuando
        # toca el suelo.
        vx, vy = 0, 0 #self.receptor.figura.obtener_velocidad_lineal()

        if self.control.izquierda:
            vx = -(self.receptor.velocidad)
            self.receptor.mover(vx)

        elif self.control.derecha:
            vx = self.receptor.velocidad
            self.receptor.mover(vx)
