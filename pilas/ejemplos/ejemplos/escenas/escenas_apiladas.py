import pilas
from pilas.escena.escena_normal import EscenaNormal

pilas.iniciar()


class EscenaDeMenu(EscenaNormal):

    def __init__(self):
        EscenaNormal.__init__(self)
        
    def iniciar(self):   
        self.id = "EscenaDeMenu"
        pilas.fondos.Selva()

        opciones = [
            ('Comenzar a jugar', self.comenzar),
            ('Opciones', self.opciones),
            ('Salir', self.salir)]

        self.menu = pilas.actores.Menu(opciones)
        
    def comenzar(self):
        pilas.cambiar_escena(EscenaDeJuego())
        
    def opciones(self):
        pilas.almacenar_escena(EscenaDeOpciones())

    def salir(self):
        import sys
        sys.exit(0)


class EscenaDeJuego(EscenaNormal):

    def __init__(self):
        EscenaNormal.__init__(self)
        
    def iniciar(self):
        self.id = "EscenaDeJuego"
        pilas.fondos.Espacio()

        self.nave = pilas.actores.Nave()
        
        #pelota1 = pilas.actores.Pingu()
        pelota2 = pilas.actores.Pelota(y=200)
        
        pilas.actores.Texto("Pulsa la tecla 'ESC' para regresar al menu \n o la tecla 'o' para ir a las opciones ...\n\
Si vas a opciones y regresas, la nave\n seguira en la misma posicion donde \n la dejaste.")

        self.pulsa_tecla_escape.conectar(self.ir_a_menu)
        
        self.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
        
        self.click_de_mouse.conectar(self.raton)
        
    def raton(self, evento):
        if self.fisica.timeStep == 0:
            self.reanudar()
        else:
            self.pausar()
        
    def ir_a_menu(self, evento):
        pilas.cambiar_escena(EscenaDeMenu())
        
    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'o':
            pilas.almacenar_escena(EscenaDeOpciones())
        if evento.texto == u'a':
            print self.actores
    
class EscenaDeOpciones(EscenaNormal):

    def __init__(self):
        EscenaNormal.__init__(self)
        
    def iniciar(self):
        self.id = "EscenaDeOpciones"
        pilas.fondos.Noche()

        opciones = [
            ('Sonido: OFF', self.nada)]

        self.menu = pilas.actores.Menu(opciones, y=200)
        pelota1 = pilas.actores.Pelota()
        
        pilas.actores.Texto("Pulsa la tecla 'ESC' para regresar.")
        self.pulsa_tecla_escape.conectar(self.ir_a_escena_anterior)

    def nada(self):
        pilas.avisar("Esto no hace nada.")

    def ir_a_escena_anterior(self, evento):
        pilas.recuperar_escena()

# Carga la nueva escena
pilas.cambiar_escena(EscenaDeMenu())
pilas.ejecutar()
