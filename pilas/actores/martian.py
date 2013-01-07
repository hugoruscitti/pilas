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
    """Es un personaje de un marciano que puede caminar, saltar y disparar.

        .. image:: images/actores/martian.png

    Este actor se puede mover con el teclado, pulsando las teclas ``izquierda``,
    ``arriba``, ``abajo`` y ``derecha`` ademas de disparar con la
    ``barra espaciadora``.

    El marciano necesita un mapa para no caer al vacio y desaparecer de la
    pantalla.

        >>> marciano = pilas.actores.Martian(pilas.actores.Mapa())

    """

    def __init__(self, mapa, x=0, y=0):
        """Constructor del marciano

        :param mapa: el mapa para que interactue el marciano.
        :type mapa: pilas.actores.Mapa
        :param x: Posición horizontal del marciano.
        :type x: int
        :param y: Posición vertical del marciano.
        :type y: int

        """
        Actor.__init__(self, x=x, y=y)
        self.imagen = pilas.imagenes.cargar_grilla("marcianitos/martian.png", 12)
        self.definir_cuadro(0)
        self.mapa = mapa
        self.hacer(Esperando())
        self.municion = pilas.actores.proyectil.Bala
        self.aprender(pilas.habilidades.Disparar,
                       municion=pilas.actores.proyectil.Bala,
                       angulo_salida_disparo=-90,
                       frecuencia_de_disparo=8,
                       offset_disparo=(25,0),
                       offset_origen_actor=(25,23))


    def definir_cuadro(self, indice):
        self.imagen.definir_cuadro(indice)
        self.definir_centro((32, 123))

    def actualizar(self):
        "Sigue el movimiento de la figura."
        pass

    def puede_saltar(self):
        return True

    def obtener_distancia_al_suelo(self):
        return self.mapa.obtener_distancia_al_suelo(self.x, self.y, 100)


#===============================================================================
# Estados del marciano
#===============================================================================

class Esperando(Comportamiento):
    "Un actor en posicion normal o esperando a que el usuario pulse alguna tecla."

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(0)

    def actualizar(self):
        if pilas.escena_actual().control.izquierda:
            self.receptor.hacer(Caminando())
        elif pilas.escena_actual().control.derecha:
            self.receptor.hacer(Caminando())

        if pilas.escena_actual().control.arriba and self.receptor.puede_saltar():
            self.receptor.hacer(Saltando(-8))

        if pilas.escena_actual().control.boton:
            self.receptor.hacer(Disparar(self.receptor))

        self.caer_si_no_toca_el_suelo()

    def caer_si_no_toca_el_suelo(self):
        if self.receptor.obtener_distancia_al_suelo() > 0:
            self.receptor.hacer(Saltando(0))

class Caminando(Esperando):

    def __init__(self):
        self.cuadros = [1, 1, 1, 2, 2, 2]
        self.paso = 0

    def iniciar(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        self.avanzar_animacion()

        if pilas.escena_actual().control.izquierda:
            self.receptor.x -= 3
            self.receptor.espejado = True
            self.receptor.habilidades.Disparar.angulo_salida_disparo = 90
        elif pilas.escena_actual().control.derecha:
            self.receptor.x += 3
            self.receptor.espejado = False
            self.receptor.habilidades.Disparar.angulo_salida_disparo = -90
        else:
            self.receptor.hacer(Esperando())

        if pilas.escena_actual().control.arriba:
            self.receptor.hacer(Saltando(-8))

        self.caer_si_no_toca_el_suelo()

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.paso])

class Saltando(Comportamiento):

    def __init__(self, velocidad_de_salto):
        self.velocidad_de_salto = velocidad_de_salto
        Comportamiento.__init__(self)

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(3)

    def actualizar(self):
        self.velocidad_de_salto += 0.25
        distancia = self.receptor.obtener_distancia_al_suelo()

        # Si toca el suelo se detiene.
        if self.velocidad_de_salto > distancia:
            self.receptor.y -= distancia
            self.receptor.hacer(Esperando())
        else:
            self.receptor.y -= self.velocidad_de_salto

        # obtiene la veloridad del personaje para detectar cuando
        # toca el suelo.
        vx, vy = 0, 0 #self.receptor.figura.obtener_velocidad_lineal()

        if pilas.escena_actual().control.izquierda:
            self.receptor.espejado = True
            self.receptor.habilidades.Disparar.angulo_salida_disparo = 90
            self.receptor.x -= 3
        elif pilas.escena_actual().control.derecha:
            self.receptor.espejado = False
            self.receptor.habilidades.Disparar.angulo_salida_disparo = -90
            self.receptor.x += 3

class Disparar(Comportamiento):

    def __init__(self, receptor):
        self.cuadros = [6, 6, 7, 7, 8, 8]
        self.paso = 0

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
