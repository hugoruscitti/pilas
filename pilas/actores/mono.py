# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class Mono(Actor):
    """Representa la cara de un mono de color marrón.

    .. image:: images/actores/mono.png

    Este personaje se usa como ejemplo básico de un actor. Por
    ejemplo, esta es una forma de usar al actor:

        >>> mono = pilas.actores.Mono()
        >>> mono.decir("Hola!!!")
        >>> mono.gritar()
    """

    def __init__(self, x=0, y=0):
        """
        Constructor del Mono.

        :param x: posicion horizontal del mono.
        :type x: int
        :param y: posicion vertical del mono.
        :type y: int

        """
        self.image_normal = pilas.imagenes.cargar('monkey_normal.png')
        self.image_smile = pilas.imagenes.cargar('monkey_smile.png')
        self.image_shout = pilas.imagenes.cargar('monkey_shout.png')

        self.sound_shout = pilas.sonidos.cargar('shout.wav')
        self.sound_smile = pilas.sonidos.cargar('smile.wav')

        # Inicializa el actor.
        Actor.__init__(self, self.image_normal, x=x, y=y)
        self.radio_de_colision = 50

    def sonreir(self):
        """Hace que el mono sonria y emita un sonido."""
        self.definir_imagen(self.image_smile)
        # Luego de un segundo regresa a la normalidad
        pilas.mundo.agregar_tarea_una_vez(2, self.normal)
        self.sound_smile.reproducir()

    def gritar(self):
        """Hace que el mono grite emitiendo un sonido."""
        self.definir_imagen(self.image_shout)
        # Luego de un segundo regresa a la normalidad
        pilas.mundo.agregar_tarea_una_vez(1, self.normal)
        self.sound_shout.reproducir()

    def normal(self):
        """Restaura la expresión del mono.

        Este función se suele ejecutar por si misma, unos
        segundos después de haber gritado y sonreir."""
        self.definir_imagen(self.image_normal)

    def decir(self, mensaje):
        """Emite un mensaje y además sonrie mientras habla.

        :param mensaje: Texto que se desea mostrar.
        :type mensaje: string

        Por ejemplo:

            >>> mono.decir("Estoy hablando!!!")

        .. image:: images/actores/mono_dice.png
        """
        self.sonreir()
        Actor.decir(self, mensaje)

    def saltar(self):
        """ Hace que el mono sonria y salte. """
        self.sonreir()
        self.hacer(pilas.comportamientos.Saltar())
