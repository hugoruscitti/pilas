# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class Boton(pilas.actores.Actor):
    
    def __init__(self, texto="", x=0, y=0, icono=None):
        pilas.actores.Actor.__init__(self, x=x, y=y)
        self.texto = texto
        self._crear_imagenes_de_botones()

        if icono:
            self.icono = pilas.imagenes.cargar(icono)
        else:
            self.icono = None

        self.imagen_normal = pilas.imagenes.cargar("interfaz/caja.png")
        self.centro = ("centro", "centro")
        
    def _crear_imagenes_de_botones(self):
        ancho, alto = pilas.utils.obtener_area_de_texto(self.texto)
        self.imagen = pilas.imagenes.cargar_superficie(20 + ancho, 30)
        tema = pilas.imagenes.cargar("boton/tema.png")

        self.imagen.pintar_parte_de_imagen(tema, 0, 0, 5, 25, 0, 0)

        for x in range(1, ancho + 20, 5):
            self.imagen.pintar_parte_de_imagen(tema, 5, 0, 5, 25, x, 0)

        self.imagen.pintar_parte_de_imagen(tema, 75, 0, 5, 25, ancho + 15, 0)
        self.imagen.texto(self.texto, 10, 17)
