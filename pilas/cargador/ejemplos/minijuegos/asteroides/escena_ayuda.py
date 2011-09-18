import pilas

MENSAJE_AYUDA = """
En Asteroides, tienes que controlar una
nave usando el teclado. El objetivo
del juego es destruir todas las piedras
del espacio disparando.

Para disparar tienes que usar la barra
espaciadora y para mover la nave
puedes usar las flechas del teclado.
"""

class Ayuda(pilas.escenas.Escena):
    "Es la escena que da instrucciones de como jugar."

    def __init__(self):
        pilas.escenas.Escena.__init__(self)
        pilas.fondos.Fondo("data/ayuda.png")
        self.crear_texto_ayuda()
        pilas.eventos.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)

    def crear_texto_ayuda(self):
        titulo = pilas.actores.Texto("Ayuda", y=200)
        texto = pilas.actores.Texto(MENSAJE_AYUDA, y=275)
        pilas.avisar("Pulsa ESC para regresar")

    def cuando_pulsa_tecla(self, *k, **kv):
        import escena_menu
        escena_menu.EscenaMenu()
