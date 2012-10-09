import pilas

class EscenaMenu(pilas.escena.Base):
    "Escena de presentacion del juego."

    def __init__(self):
        pilas.escena.Base.__init__(self)
        
    def iniciar(self):
        pilas.fondos.Fondo('data/inicio.png')
        self.menu_de_juego()

    def menu_de_juego(self):
        opciones_menu = [
        ("Iniciar juego", self.iniciar_juego),
        ("Ayuda", self.mostrar_ayuda),
        ("Salir", self.salir_del_juego),
        ]
        self.menu = pilas.actores.Menu(opciones_menu, y = -50)

    def iniciar_juego(self):
        import escena_juego
        pilas.cambiar_escena(escena_juego.Juego())

    def salir_del_juego(self):
        pilas.terminar()

    def mostrar_ayuda(self):
        import escena_ayuda
        pilas.cambiar_escena(escena_ayuda.Ayuda())
