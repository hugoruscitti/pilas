# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class Energia(Actor):
    """Representa un indicador de energia (en forma de barra horizontal)."""

    def __init__(self, x=0, y=0, progreso=50, ancho=200, alto=30):
        Actor.__init__(self, x=x, y=y)
        self.area_ancho = ancho
        self.area_alto = alto
        self.progreso = progreso
        self.progreso_anterior = progreso
        self.imagen = pilas.imagenes.cargar_superficie(self.area_ancho, self.area_alto)
        self.pintar_imagen()
        self.fijo = True

    def pintar_imagen(self):
        self.imagen.limpiar()
        #self.imagen.pintar(pilas.colores.negro)
        color_relleno = pilas.colores.amarillo

        area = self.area_ancho / 100.0
        self.imagen.rectangulo(0, 0, area * self.progreso, self.area_alto, 
                                    color=color_relleno, relleno=True)
        
        # Borde exterior
        self.imagen.rectangulo(1, 1, self.area_ancho-2, self.area_alto-2, 
                               color=pilas.colores.negro, relleno=False, grosor=2)

    def actualizar(self):
        if self.progreso_anterior != self.progreso:
            # Carga el progreso y lo actualiza pero siempre entre 0 y 100
            self.progreso_anterior = self.progreso
            self.pintar_imagen()
