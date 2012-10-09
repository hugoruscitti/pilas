import pilas
import piedra_espacial
import random

class Estado:
    "Representa una escena dentro del juego."

    def actualizar(self):
        raise Exception("Tienes que sobrescribir este metodo...")

class Jugando(Estado):
    "Representa el estado de juego."

    def __init__(self, juego, nivel):
        self.nivel = nivel
        self.juego = juego
        self.juego.crear_naves(cantidad=nivel * 3)

        # Cada un segundo le avisa al estado que cuente.
        pilas.mundo.agregar_tarea(1, self.actualizar)

    def actualizar(self):
        if self.juego.ha_eliminado_todas_las_piedras():
            self.juego.cambiar_estado(Iniciando(self.juego, self.nivel + 1))
            return False

        return True

class Iniciando(Estado):
    "Estado que indica que el juego ha comenzado."

    def __init__(self, juego, nivel):
        self.texto = pilas.actores.Texto("Iniciando el nivel %d" %(nivel))
        self.nivel = nivel
        self.texto.color = pilas.colores.blanco
        self.contador_de_segundos = 0
        self.juego = juego

        # Cada un segundo le avisa al estado que cuente.
        pilas.mundo.agregar_tarea(1, self.actualizar)

    def actualizar(self):
        self.contador_de_segundos += 1

        if self.contador_de_segundos > 2:
            self.juego.cambiar_estado(Jugando(self.juego, self.nivel))
            self.texto.eliminar()
            return False

        return True    # para indicarle al contador que siga trabajado.

class PierdeVida(Estado):

    def __init__(self, juego):
        self.contador_de_segundos = 0
        self.juego = juego

        if self.juego.contador_de_vidas.le_quedan_vidas():
            self.juego.contador_de_vidas.quitar_una_vida()
            pilas.mundo.agregar_tarea(1, self.actualizar)
        else:
            juego.cambiar_estado(PierdeTodoElJuego(juego))

    def actualizar(self):
        self.contador_de_segundos += 1

        if self.contador_de_segundos > 2:
            self.juego.crear_nave()
            return False

        return True

class PierdeTodoElJuego(Estado):

    def __init__(self, juego):
        # Muestra el mensaje "has perdido"
        mensaje = pilas.actores.Texto("Lo siento, has perdido!")
        mensaje.color=pilas.colores.blanco
        mensaje.abajo = 240
        mensaje.abajo = [-20]

    def actualizar(self):
        pass


class Juego(pilas.escena.Base):
    "Es la escena que permite controlar la nave y jugar"

    def __init__(self):
        pilas.escena.Base.__init__(self)
        
    def iniciar(self):        
        pilas.fondos.Espacio()
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)
        self.piedras = []
        self.crear_nave()
        self.crear_contador_de_vidas()
        self.cambiar_estado(Iniciando(self, 1))
        self.puntaje = pilas.actores.Puntaje(x=280, y=220, color=pilas.colores.blanco)

    def cambiar_estado(self, estado):
        self.estado = estado

    def crear_nave(self):
        nave = pilas.actores.Nave()
        nave.aprender(pilas.habilidades.SeMantieneEnPantalla)
        nave.definir_enemigos(self.piedras, self.cuando_explota_asterioide)
        self.colisiones.agregar(nave, self.piedras, self.explotar_y_terminar)

    def cuando_explota_asterioide(self):
        self.puntaje.aumentar(1)

    def crear_contador_de_vidas(self):
        import contador_de_vidas
        self.contador_de_vidas = contador_de_vidas.ContadorDeVidas(3)

    def cuando_pulsa_tecla_escape(self, *k, **kv):
        "Regresa al menu principal."
        import escena_menu
        pilas.cambiar_escena(escena_menu.EscenaMenu())

    def explotar_y_terminar(self, nave, piedra):
        "Responde a la colision entre la nave y una piedra."
        nave.eliminar()

        self.cambiar_estado(PierdeVida(self))

    def crear_naves(self, cantidad):
        "Genera una cantidad especifica de naves en el escenario."
        fuera_de_la_pantalla = [-600, -650, -700, -750, -800]
        tamanos = ['grande', 'media', 'chica']

        for x in range(cantidad):
            x = random.choice(fuera_de_la_pantalla)
            y = random.choice(fuera_de_la_pantalla)
            t = random.choice(tamanos)

            piedra_nueva = piedra_espacial.PiedraEspacial(self.piedras, x=x, y=y, tamano=t)
            self.piedras.append(piedra_nueva)

    def ha_eliminado_todas_las_piedras(self):
        return len(self.piedras) == 0
