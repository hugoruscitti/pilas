# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PySFML import sf

import pilas


class Habilidad:

    def __init__(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        pass


class RebotaComoPelota(Habilidad):

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        self.figura = pilas.fisica.fisica.crear_figura_circulo(receptor.x, 
                                                               receptor.y, 
                                                               receptor.radio_de_colision,
                                                               masa=1,
                                                               elasticidad=0)
        
    def actualizar(self):
        self.receptor.x = self.figura.body.position.x
        self.receptor.y = self.figura.body.position.y
        self.receptor.rotacion = self.figura.body.angle * 1000

class ColisionableComoPelota(RebotaComoPelota):

    def __init__(self, receptor):
        RebotaComoPelota.__init__(self, receptor)
        
    def actualizar(self):
        self.figura.body.position.x = self.receptor.x
        self.figura.body.position.y = self.receptor.y


class SeguirAlMouse(Habilidad):
    "Hace que un actor siga la posición del mouse en todo momento."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.eventos.mueve_mouse.connect(self.mover)

    def mover(self, sender, x, y, signal):
        self.receptor.x = x
        self.receptor.y = y

class AumentarConRueda(Habilidad):
    "Permite cambiar el tamaño de un actor usando la ruedita scroll del mouse."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.eventos.mueve_rueda.connect(self.cambiar_de_escala)

    def cambiar_de_escala(self, sender, delta, signal):
        self.receptor.escala += (delta / 4.0)


class SeguirClicks(Habilidad):
    "Hace que el actor se coloque la posición del cursor cuando se hace click."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.eventos.click_de_mouse.connect(self.moverse_a_este_punto)

    def moverse_a_este_punto(self, sender, signal, x, y, button):
        self.receptor.x = pilas.interpolar(x, duracion=0.5)
        self.receptor.y = pilas.interpolar(y, duracion=0.5)


class Arrastrable(Habilidad):
    """Hace que un objeto se pueda arrastrar con el puntero del mouse.

    Cuando comienza a mover al actor se llama al metodo ''comienza_a_arrastrar''
    y cuando termina llama a ''termina_de_arrastrar''. Estos nombres
    de metodos se llaman para que puedas personalizar estos eventos, dado
    que puedes usar polimorfismo para redefinir el comportamiento
    de estos dos metodos. Observa un ejemplo de esto en
    el ejemplo ``pilas.ejemplos.Piezas``.
    """

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.eventos.click_de_mouse.connect(self.try_to_drag)

    def try_to_drag(self, sender, signal, x, y, button):
        "Intenta mover el objeto con el mouse cuando se pulsa sobre el."

        if self.receptor.colisiona_con_un_punto(x, y):
            pilas.eventos.termina_click.connect(self.drag_end)
            pilas.eventos.mueve_mouse.connect(self.drag, uid='drag')
            self.comienza_a_arrastrar()

    def drag(self, sender, signal, x, y, dx, dy):
        "Arrastra el actor a la posicion indicada por el puntero del mouse."
        self.receptor.x += dx
        self.receptor.y += dy

    def drag_end(self, sender, signal, x, y, button):
        "Suelta al actor porque se ha soltado el botón del mouse."
        pilas.eventos.mueve_mouse.disconnect(uid='drag')
        self.termina_de_arrastrar()

    def comienza_a_arrastrar(self):
        pass

    def termina_de_arrastrar(self):
        pass

class MoverseConElTeclado(Habilidad):
    "Hace que un actor cambie de posición con pulsar el teclado."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.eventos.actualizar.connect(self.on_key_press)

    def on_key_press(self, sender, signal):
        velocidad = 5
        c = pilas.mundo.control

        if c.izquierda:
            self.receptor.x -= velocidad
        elif c.derecha:
            self.receptor.x += velocidad

        if c.arriba:
            self.receptor.y += velocidad
        elif c.abajo:
            self.receptor.y -= velocidad
