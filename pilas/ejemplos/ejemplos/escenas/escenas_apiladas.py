import pilas
from pilas.escena import Normal
from pilas.escena import Pausa


class EscenaDeMenu(pilas.escena.Normal):

    def __init__(self):
        Normal.__init__(self)

    def iniciar(self):
        pilas.fondos.Color(pilas.colores.negro)

        pilas.actores.Texto("Bienvenidos al ejemplo de escenas apiladas.",
                            y=200)

        opciones = [
            ('Cambiar a Escena 1', self.cambiar_escena_1),
            ('Almacenar y Cambiar a Escena 2', self.cambiar_escena_2),
            ('Salir', self.salir)]

        self.menu = pilas.actores.Menu(opciones)

    def cambiar_escena_1(self):
        pilas.cambiar_escena(Escena_1())

    def cambiar_escena_2(self):
        pilas.almacenar_escena(Escena_2())

    def salir(self):
        import sys
        sys.exit(0)


class Escena_1(pilas.escena.Normal):

    def __init__(self):
        Normal.__init__(self)

    def iniciar(self):
        pilas.actores.Texto("Acabas de cambiar a la Escena 1.\n\
Intenta mover la nave por la pantalla con el teclado.",
                            y=200)

        pilas.actores.Texto("Pulsa la tecla 'ESC' para regresar al menu \n\
        , la tecla '2' para ir a la Escena 2\n\n\
        o la tecla 'p' para Pausar\n\n\
Si vas a la Escena 2 y regresas, la nave\n\
seguira en la misma posicion donde la dejaste.")

        self.nave = pilas.actores.Nave()

        self.pulsa_tecla_escape.conectar(self.ir_a_menu)

        self.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def ir_a_menu(self, evento):
        pilas.cambiar_escena(EscenaDeMenu())

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'2':
            pilas.almacenar_escena(Escena_2())
        if evento.texto == u'a':
            print(self.actores)
        if evento.texto == u'p':
            pilas.escena.pausar()


class Escena_2(pilas.escena.Normal):

    def __init__(self):
        Normal.__init__(self)

    def iniciar(self):
        pilas.fondos.Tarde()

        pilas.actores.Texto("Acabas de cambiar a la Escena 2.", y=200)

        pilas.actores.Texto("Pulsa la tecla 'ESC' para regresar a la\n\
        escena anterior.")

        self.pulsa_tecla_escape.conectar(self.ir_a_escena_anterior)

    def ir_a_escena_anterior(self, evento):
        pilas.recuperar_escena()

pilas.iniciar()
pilas.cambiar_escena(EscenaDeMenu())
pilas.ejecutar()
