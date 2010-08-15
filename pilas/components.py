# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class MovedByMouse:
    "Hace que un actor siga la posición del mouse en todo momento."

    def __init__(self):
        pilas.signals.mouse_move.connect(self.move)

    def move(self, sender, x, y, signal):
        self.x = x
        self.y = y


class SizeByWheel:
    "Permite cambiar el tamaño de un actor usando la ruedita scroll del mouse."

    def __init__(self):
        pilas.signals.mouse_wheel.connect(self.scale_me)

    def scale_me(self, sender, delta, signal):
        self.scale += (delta / 2.0)


class FollowMouseClicks:
    "Hace que el actor se coloque la posición del cursor cuando se hace click."

    def __init__(self):
        pilas.signals.mouse_click.connect(self.move_to_this_point)

    def move_to_this_point(self, sender, signal, x, y, button):
        self.x = pilas.interpolate(x, duration=0.5)
        self.y = pilas.interpolate(y, duration=0.5)
