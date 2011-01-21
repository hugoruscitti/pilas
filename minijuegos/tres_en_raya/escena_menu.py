import pilas

class EscenaMenu(pilas.escenas.Escena):
    "Escena de presentacion del juego."

    def __init__(self):
        pilas.actores.utils.eliminar_a_todos()
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
        self.menu.desactivar()
        import escena_juego
        escena_juego.Juego()

    def salir_del_juego(self):
        pilas.terminar()

    def mostrar_ayuda(self):
        self.menu.desactivar()
        import escena_ayuda
        escena_ayuda.Ayuda()
