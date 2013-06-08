# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Boton

class Sonido(Boton):
    """Un icono de sonido en la parte inferior derecha de la pantalla.

    Este actor se utilizará para habilitar el sonido o deshabilitarlo al
    hacer click sobre él.
    """

    def __init__(self, x=0, y=0):
        """Inicializa actor que permite controlar el sonido."""
        # TODO: quitar x e y de los argumentos, ya se no se utilizan.
        Boton.__init__(self, x=0, y=0, ruta_normal = 'iconos/sonido_on.png',
                       ruta_press = 'iconos/sonido_off.png')

        self.conectar_presionado(self.deshabilitar_sonido)

        # Colocamos el boton en la esquina inferior derecha de la pantalla.
        self._ancho_mundo, self._alto_mundo = pilas.mundo.obtener_area()
        self.x = (self._ancho_mundo / 2) - self.ancho
        self.y = -1 * (self._alto_mundo / 2) + self.alto

        self.activado = True

    def deshabilitar_sonido(self):
        """Alterna entre sonido habilitado o deshabilitado."""
        if self.activado:
            pilas.mundo.deshabilitar_musica()
            pilas.mundo.deshabilitar_sonido()
            self.pintar_presionado()
            pilas.avisar("Sonido deshabilitado")
            self.activado = False
        else:
            pilas.mundo.deshabilitar_musica(estado=False)
            pilas.mundo.deshabilitar_sonido(estado=False)
            self.pintar_normal()
            pilas.avisar("Sonido habilitado")
            self.activado = True
