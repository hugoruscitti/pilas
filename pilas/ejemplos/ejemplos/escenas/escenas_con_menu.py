import pilas

pilas.iniciar()


class EscenaDeMenu(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        pilas.fondos.Selva()

        opciones = [
		    ('Comenzar a jugar', self.comenzar),
		    ('Salir', self.salir)]

        self.menu = pilas.actores.Menu(opciones)

    def comenzar(self):
        pilas.cambiar_escena(EscenaDeJuego())

    def salir(self):
        import sys
        sys.exit(0)


class EscenaDeJuego(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        self.pingu = pilas.actores.Pingu()
        pilas.fondos.Pasto()
        pilas.avisar("Pulsa la tecla 'q' para regresar al menu...")

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'q':
            pilas.cambiar_escena(EscenaDeMenu())
	
# Carga la nueva escena
pilas.cambiar_escena(EscenaDeMenu())
pilas.ejecutar()
