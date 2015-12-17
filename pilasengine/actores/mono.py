# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Mono(Actor):

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = "mono.png"
        self.sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        self.imagen_normal = self.pilas.imagenes.cargar("mono.png")
        self.imagen_reir = self.pilas.imagenes.cargar("mono_reir.png")
        self.imagen_gritar = self.pilas.imagenes.cargar("mono_gritar.png")

        self.imagen = self.imagen_normal
        self.sonido_reir = self.pilas.sonidos.cargar('audio/smile.wav')
        self.sonido_gritar = self.pilas.sonidos.cargar('audio/grito.wav')
        self.radio_de_colision = 50

    def iniciar(self, *k, **kw):
        pass

    def normal(self):
        """Restaura la expresión del mono.

        Este función se suele ejecutar por si misma, unos
        segundos después de haber gritado y sonreir."""
        self.imagen = self.imagen_normal

    def sonreir(self):
        """Hace que el mono sonria y emita un sonido."""
        self.imagen = self.imagen_reir
        self.pilas.tareas.una_vez(2, self.normal)
        self.sonido_reir.reproducir()

    def gritar(self):
        """Hace que el mono grite emitiendo un sonido."""
        self.imagen = self.imagen_gritar
        self.pilas.tareas.una_vez(2, self.normal)
        self.sonido_gritar.reproducir()

    def decir(self, mensaje):
        """Emite un mensaje y además sonrie mientras habla."""
        self.sonreir()
        super(Mono, self).decir(mensaje)

    def saltar(self):
        """ Hace que el mono sonria y salte. """
        self.sonreir()
        self.hacer(self.pilas.comportamientos.Saltar)
