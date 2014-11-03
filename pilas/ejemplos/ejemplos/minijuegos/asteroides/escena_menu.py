import pilas
import random

class EscenaMenu(pilas.escena.Base):
    "Es la escena de presentacion donde se elijen las opciones del juego."

    def __init__(self):
        pilas.escena.Base.__init__(self)
    
    def iniciar(self):
        pilas.fondos.Fondo("data/menu.png")
        self.crear_titulo_del_juego()
        pilas.avisar("Use el teclado para controlar el menu.")
        self.crear_el_menu_principal()
        self.crear_asteroides()

    def crear_titulo_del_juego(self):
        logotipo = pilas.actores.Actor("data/titulo.png")
        logotipo.y = 300
        logotipo.y = [200]

    def crear_el_menu_principal(self):
        opciones = [
                    ("Comenzar a jugar", self.comenzar_a_jugar),
                    ("Ver ayuda", self.mostrar_ayuda_del_juego),
                    ("Salir", self.salir_del_juego),
                   ]
        self.menu = pilas.actores.Menu(opciones, y=-50)

    def comenzar_a_jugar(self):
        from . import escena_juego
        pilas.cambiar_escena(escena_juego.Juego())

    def mostrar_ayuda_del_juego(self):
        from . import escena_ayuda
        pilas.cambiar_escena(escena_ayuda.Ayuda())

    def salir_del_juego(self):
        pilas.terminar()

    def crear_asteroides(self):
        fuera_de_la_pantalla = [-600, -650, -700, -750, -800]
        from . import piedra_espacial
        for x in range(5):
            x = random.choice(fuera_de_la_pantalla)
            y = random.choice(fuera_de_la_pantalla)
            piedra_espacial.PiedraEspacial([], x=x, y=y, tamano="chica")
