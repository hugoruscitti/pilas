# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Fantasma(Actor):
    """Representa al fantasman del clasico pac-man."""
    
    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.grilla = self.pilas.imagenes.cargar_grilla("fantasma.png", 8, 1)
        self.imagen = self.grilla
        self.cuadro = 0
        self.control = self.pilas.escena_actual().control
        self.velocidad = 3
        self.posicion = 0  # 0 = para arriba, 1 = para abajo,
                           # 2 = para izquierda, 3 = para derecha

    def actualizar(self):
        if self.control.izquierda:
            self.posicion = 2
            self.x -= self.velocidad
            self._reproducir_animacion()
        elif self.control.derecha:
            self.posicion = 3
            self.x += self.velocidad
            self._reproducir_animacion()
        elif self.control.abajo:
            self.posicion = 1
            self.y -= self.velocidad
            self._reproducir_animacion()
        elif self.control.arriba:
            self.posicion = 0
            self.y += self.velocidad
            self._reproducir_animacion()

    def _reproducir_animacion(self):
        self.cuadro += 0.2

        if self.cuadro > 1:
            self.cuadro = 0

        self.definir_cuadro(int(self.posicion * 2 + self.cuadro))

    def definir_cuadro(self, indice):
        """Cambia el cuadro de animación a mostrar.

        :param indice: Número de cuadro a mostrar.
        """
        self.imagen.definir_cuadro(indice)