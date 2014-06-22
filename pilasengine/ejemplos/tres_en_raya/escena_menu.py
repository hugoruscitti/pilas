# -*- encoding: utf-8 -*-
from pilasengine.escenas import normal
from pilasengine.fondos import fondo


class FondoEscenaMenu(fondo.Fondo):

    def iniciar(self):
        self.imagen = './data/inicio.png'


class EscenaMenu(normal.Normal):
    """Escena de presentacion del juego."""

    def iniciar(self):
        self.fondo = FondoEscenaMenu(self.pilas)
        self.menu_de_juego()

    def menu_de_juego(self):
        opciones_menu = [("Iniciar juego", self.iniciar_juego),
                         ("Ayuda", self.mostrar_ayuda),
                         ("Salir", self.salir_del_juego)]
        self.menu = self.pilas.actores.Menu(opciones_menu, y=-50)

    def iniciar_juego(self):
        import escena_juego
        self.pilas.escenas.definir_escena(escena_juego.EscenaJuego(self.pilas))

    def salir_del_juego(self):
        self.pilas.terminar()

    def mostrar_ayuda(self):
        import escena_ayuda
        self.pilas.escenas.definir_escena(escena_ayuda.EscenaAyuda(self.pilas))