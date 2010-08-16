# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PySFML import sf

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


class Draggable:
    "Hace que un objeto se pueda arrastrar con el puntero del mouse."

    def __init__(self):
        pilas.signals.mouse_click.connect(self.try_to_drag)

    def try_to_drag(self, sender, signal, x, y, button):
        "Intenta mover el objeto con el mouse cuando se pulsa sobre el."

        if self.collide_with_point(x, y):
            pilas.signals.mouse_click_end.connect(self.drag_end)
            pilas.signals.mouse_move.connect(self.drag, dispatch_uid='drag')
            self.last_x = x
            self.last_y = y

    def drag(self, sender, signal, x, y):
        "Arrastra el actor a la posicion indicada por el puntero del mouse."
        self.x += x - self.last_x
        self.y += y - self.last_y

        self.last_x = x
        self.last_y = y

    def drag_end(self, sender, signal, x, y, button):
        "Suelta al actor porque se ha soltado el botón del mouse."
        pilas.signals.mouse_move.disconnect(dispatch_uid='drag')


class MovedByKeyboard:
    "Hace que un actor cambie de posición con pulsar el teclado."

    def __init__(self):
        pilas.signals.key_press.connect(self.on_key_press)

    def on_key_press(self, sender, code, signal):
        speed = 10

        if code == sf.Key.Left:
            self.x -= speed
        elif code == sf.Key.Right:
            self.x += speed

        if code == sf.Key.Up:
            self.y -= speed
        elif code == sf.Key.Down:
            self.y += speed

