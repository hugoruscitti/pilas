import pilas
from pilas.escenas import Normal

pilas.iniciar()


class EscenaDeMenu(Normal):

    def __init__(self):
        Normal.__init__(self)
        pilas.fondos.Selva()

        opciones = [
		    ('Comenzar a jugar', self.comenzar),
		    ('Salir', self.salir)]

        self.menu = pilas.actores.Menu(opciones)

    def comenzar(self):
        pilas.mundo.definir_escena(EscenaDeJuego())

    def salir(self):
        import sys
        sys.exit(0)


class EscenaDeJuego(Normal):

    def __init__(self):
        Normal.__init__(self)
        pingu = pilas.actores.Pingu()
        pilas.fondos.Pasto()
        pilas.avisar("Pulsa la tecla 'q' para regresar al menu...")

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'q':
            pilas.mundo.definir_escena(EscenaDeMenu())
	
pilas.mundo.definir_escena(EscenaDeMenu())
pilas.ejecutar()
