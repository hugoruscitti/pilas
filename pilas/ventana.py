# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PySFML import sf

def iniciar(ancho=640, alto=480, titulo="Pilas"):
    return sf.RenderWindow(sf.VideoMode(ancho, alto), titulo)

