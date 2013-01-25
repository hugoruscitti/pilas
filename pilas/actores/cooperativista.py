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

VELOCIDAD = 4

class Cooperativista(Actor):
    """ Representa un Cooperativista que puede caminar y trabajar."""

    def __init__(self, x=0, y=0):
        """Constructor del Cooperativista

        :param x: Posición horizontal de la aceituna.
        :type x: int
        :param y: Posición vertical de la aceituna.
        :type y: int
        """
        Actor.__init__(self, x=x, y=y)
        self._cargar_animaciones()
        self.hacer(Esperando())
        self.radio_de_colision = 30

    def _cargar_animaciones(self):
        cargar = pilas.imagenes.cargar_grilla
        self.animaciones = {
            "ok": cargar("cooperativista/ok.png", 1),
            "parado": cargar("cooperativista/parado.png", 1),
            "camina": cargar("cooperativista/camina.png", 4),
            # las siguientes estan sin usar...
            "alerta": cargar("cooperativista/alerta.png", 2),
            "trabajando": cargar("cooperativista/trabajando.png", 1),
            "parado_sujeta": cargar("cooperativista/parado_sujeta.png", 1),
            "camina_sujeta": cargar("cooperativista/camina_sujeta.png", 4),
            }

    def definir_cuadro(self, indice):
        """Define el cuadro de la animación del actor.

        :param indice: el cuadro que la animación que se quiere mostrar.
	    """
        self.imagen.definir_cuadro(indice)

    def cambiar_animacion(self, nombre):
        """Cambia la animación del Cooperativista.

        :param nombre: El nombre de la animación que se quiere mostar.
	    """
        self.imagen = self.animaciones[nombre]
        self.centro = ("centro", "abajo")

class Esperando(Comportamiento):
    """Clase que define un comportamiento del actor Cooperativista."""

    def iniciar(self, receptor):
        """Inicializa el comportamiento.

        :param receptor: La referencia al actor.
        """
        self.receptor = receptor
        self.receptor.cambiar_animacion("parado")
        self.receptor.definir_cuadro(0)

    def actualizar(self):
        if pilas.escena_actual().control.izquierda:
            self.receptor.hacer(Caminando())
        elif pilas.escena_actual().control.derecha:
            self.receptor.hacer(Caminando())

        if pilas.escena_actual().control.arriba:
            self.receptor.hacer(DecirOk())


class Caminando(Comportamiento):
    """Clase que define un comportamiento del actor Cooperativista."""

    def __init__(self):
        self.cuadros = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
        self.paso = 0

    def iniciar(self, receptor):
        """Inicializa el comportamiento.

        :param receptor: La referencia al actor.
        """
        self.receptor = receptor
        self.receptor.cambiar_animacion("camina")

    def actualizar(self):
        self.avanzar_animacion()

        if pilas.escena_actual().control.izquierda:
            self.receptor.x -= VELOCIDAD
            self.receptor.espejado = False
        elif pilas.escena_actual().control.derecha:
            self.receptor.x += VELOCIDAD
            self.receptor.espejado = True
        else:
            self.receptor.hacer(Esperando())

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.paso])


class DecirOk(Comportamiento):
    """Clase que define un comportamiento del actor Cooperativista."""

    def __init__(self):
        self.paso = 0

    def iniciar(self, receptor):
        """Inicializa el comportamiento.

        :param receptor: La referencia al actor.
        """
        self.receptor = receptor
        self.receptor.cambiar_animacion("ok")

    def actualizar(self):
        self.paso += 1

        if self.paso > 50:
            self.receptor.hacer(Esperando())
