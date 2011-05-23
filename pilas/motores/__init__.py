# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import motor

disponibles = []

try:
    from PySFML import sf
    disponibles.append('sfml')
except ImportError:
    pass

try:
    import pygame
    disponibles.append('pygame')
except ImportError:
    pass

try:
    import PySide
    disponibles.append('qt')
except ImportError:
    pass


# Incorpora todo el contenido de los motores, pero
# lo hace fuera del bloque try except para hacer
# fluir las excepciones.
if 'sfml' in disponibles:
    from motor_sfml import *

if 'pygame' in disponibles:
    from motor_pygame import *

if 'qt' in disponibles:
    from motor_qt import *
