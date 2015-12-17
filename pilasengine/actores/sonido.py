# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class Sonido(Actor):
    """Un icono de sonido en la parte inferior derecha de la pantalla.

    Este actor se utilizará para habilitar el sonido o deshabilitarlo al
    hacer click sobre él.
    """

    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y

        self.ruta_normal = 'iconos/sonido_on.png'
        self.ruta_press = 'iconos/sonido_off.png'

        self.imagen = self.ruta_normal
        self.radio_de_colision = 15
        
        self.cuando_hace_click = self.cuando_pulsa

        # Colocamos el boton en la esquina inferior derecha de la pantalla.
        self._ancho_mundo, self._alto_mundo = self.pilas.widget.obtener_area()
        self.x = (self._ancho_mundo / 2) - self.ancho
        self.y = -1 * (self._alto_mundo / 2) + self.alto

        self.activado = True

    def cuando_pulsa(self):
        """Alterna entre sonido habilitado o deshabilitado."""
        if self.activado:
            self.pilas.deshabilitar_musica()
            self.pilas.deshabilitar_sonido()
            self.imagen = self.ruta_press
            self.pilas.avisar("Sonido deshabilitado")
            self.activado = False
        else:
            self.pilas.deshabilitar_musica(estado=False)
            self.pilas.deshabilitar_sonido(estado=False)
            self.imagen = self.ruta_normal
            self.pilas.avisar("Sonido habilitado")
            self.activado = True
