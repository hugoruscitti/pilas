# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PySFML import sf

import pilas

class SeguirAlMouse:
    "Hace que un actor siga la posición del mouse en todo momento."

    def __init__(self):
        pilas.eventos.mueve_mouse.connect(self.move)

    def move(self, sender, x, y, signal):
        self.x = x
        self.y = y


class AumentarConRueda:
    "Permite cambiar el tamaño de un actor usando la ruedita scroll del mouse."

    def __init__(self):
        pilas.eventos.mueve_rueda.connect(self.scale_me)

    def scale_me(self, sender, delta, signal):
        self.escala += (delta / 2.0)


class SeguirClicks:
    "Hace que el actor se coloque la posición del cursor cuando se hace click."

    def __init__(self):
        pilas.eventos.click_de_mouse.connect(self.move_to_this_point)

    def move_to_this_point(self, sender, signal, x, y, button):
        self.x = pilas.interpolar(x, duration=0.5)
        self.y = pilas.interpolar(y, duration=0.5)


class Arrastrable:
    "Hace que un objeto se pueda arrastrar con el puntero del mouse."

    def __init__(self):
        pilas.eventos.click_de_mouse.connect(self.try_to_drag)

    def try_to_drag(self, sender, signal, x, y, button):
        "Intenta mover el objeto con el mouse cuando se pulsa sobre el."

        if self.colisiona_con_un_punto(x, y):
            pilas.eventos.termina_click.connect(self.drag_end)
            pilas.eventos.mueve_mouse.connect(self.drag, dispatch_uid='drag')
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
        pilas.eventos.mueve_mouse.disconnect(dispatch_uid='drag')


class MoverseConElTeclado:
    "Hace que un actor cambie de posición con pulsar el teclado."

    def __init__(self):
        pilas.eventos.pulsa_tecla.connect(self.on_key_press)

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

