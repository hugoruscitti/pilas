# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PySFML import sf
import actores

modo_depuracion = False
eje_coordenadas = None

def iniciar(ancho, alto, titulo):
    ventana = sf.RenderWindow(sf.VideoMode(ancho, alto), titulo)

    # Define que la coordenada (0, 0) sea el centro de la ventana.
    view = ventana.GetDefaultView()
    view.SetCenter(0, 0)

    return ventana

def cambiar_escala(ventana, nueva_escala):
    nuevo_ancho = ancho * nueva_escala
    nuevo_alto = alto * nueva_escala
    ventana.SetSize(int(nuevo_ancho), int(nuevo_alto))
