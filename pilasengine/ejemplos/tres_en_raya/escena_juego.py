# -*- encoding: utf-8 -*-
import random

from pilasengine.escenas import normal
from pilasengine.fondos import fondo


class FondoEscenaJuego(fondo.Fondo):

    def iniciar(self):
        self.imagen = './data/fondo.png'


class EscenaJuego(normal.Normal):

    def iniciar(self):
        self.fondo = FondoEscenaJuego(self.pilas)

        self.tablero = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]

        self.hay_ganador = False
        self.turno = "ficha{}".format(str(random.randint(1, 2)))
        self.crear_actor_turno_actual()
        self.definir_imagen_turno_actual()
        self.turnos = 9
        self.ter_ficha1 = ["ficha1", "ficha1", "ficha1"]
        self.ter_ficha2 = ["ficha2", "ficha2", "ficha2"]

        self.crear_pizarra()
        self.crear_casillas_vacias()
        self.pulsa_tecla_escape.conectar(self.cuando_se_presione_escape)

    def cuando_se_presione_escape(self, evento):
        "Regresa al menu principal"
        import escena_menu
        self.pilas.escenas.definir_escena(escena_menu.EscenaMenu(self.pilas))

    def crear_actor_turno_actual(self):
        self.turno_actual = self.pilas.actores.Actor()
        self.turno_actual.x = -160
        self.turno_actual.y = 75
        self.turno_actual.escala = .6

    def definir_imagen_turno_actual(self):
        self.turno_actual.imagen = './data/{}.png'.format(self.turno)

    def crear_casillas_vacias(self):
        self.casillas = self.pilas.actores.Grupo()
        for fila, _ in enumerate(self.tablero):
            for columna, _ in enumerate(self.tablero[fila]):
                casilla = self.pilas.actores.Boton(80*columna-80, -80*fila+80,
                                                   './data/ficha_vacia.png')
                casilla.pos_en_tablero = (fila, columna)
                casilla.conectar_presionado(self.cuando_presiona_casilla,
                                            casilla)
                self.casillas.agregar(casilla)

    def cuando_presiona_casilla(self, casilla):
        casilla.desactivar()
        imagen = './data/{}.png'.format(self.turno)
        casilla.pintar_presionado(imagen)
        casilla.escala = .8
        casilla.escala = [1]
        self.quitar_un_turno()
        self.poner_ficha_en_tablero(casilla.pos_en_tablero)
        self.verificar_ganador()
        self.verificar_empate()
        self.cambiar_turno()

    def verificar_ganador(self):
        if (self.verificar_ganador_en_horizontal() or
                self.verificar_ganador_en_vertical() or
                self.verificar_ganador_en_diagonal()):
            self.hay_ganador = True
            self.casillas.desactivar()
            self.mostrar_mensaje_fin_juego()

    def mostrar_mensaje_fin_juego(self, empate=False):
        if empate:
            mensaje = u"¡Nadie Ganó, vuelve a intentarlo!"
        else:
            nombre_jugador = self.turno.replace("ficha", "jugador ")
            mensaje = u"¡Ganó {}!".format(nombre_jugador)

        texto = self.pilas.actores.Texto(cadena_de_texto=mensaje, y=-180)
        texto.escala = .7
        texto.escala = [1]

    def verificar_empate(self):
        if not self.hay_ganador and self.turnos < 1:
            self.casillas.desactivar()
            self.mostrar_mensaje_fin_juego(empate=True)

    def verificar_ganador_en_horizontal(self):
        if self.ter_ficha1 in self.tablero:
            fila = self.tablero.index(self.ter_ficha1)
            self.pintar_linea_horizontal(fila)
            return True
        elif self.ter_ficha2 in self.tablero:
            fila = self.tablero.index(self.ter_ficha2)
            self.pintar_linea_horizontal(fila)
            return True
        return False

    def verificar_ganador_en_vertical(self):
        cols = [list(col) for col in zip(*self.tablero)]

        if self.ter_ficha1 in cols:
            columna = cols.index(self.ter_ficha1)
            self.pintar_linea_vertical(columna)
            return True
        elif self.ter_ficha2 in cols:
            columna = cols.index(self.ter_ficha2)
            self.pintar_linea_vertical(columna)
            return True
        return False

    def verificar_ganador_en_diagonal(self):
        diagonal1 = [self.tablero[0][0],
                     self.tablero[1][1],
                     self.tablero[2][2]]

        diagonal2 = [self.tablero[0][2],
                     self.tablero[1][1],
                     self.tablero[2][0]]

        if diagonal1 == self.ter_ficha1 or diagonal1 == self.ter_ficha2:
            self.pintar_linea_diagonal_1()
            return True
        elif diagonal2 == self.ter_ficha1 or diagonal2 == self.ter_ficha2:
            self.pintar_linea_diagonal_2()
            return True
        return False

    def cambiar_turno(self):
        if self.turno == "ficha1":
            self.turno = "ficha2"
        else:
            self.turno = "ficha1"
        self.definir_imagen_turno_actual()

    def quitar_un_turno(self):
        self.turnos -= 1

    def poner_ficha_en_tablero(self, casilla_pos):
        fila, columna = casilla_pos
        self.tablero[fila][columna] = self.turno

    def crear_pizarra(self):
        self.pizarra = self.pilas.actores.Pizarra()

    def pintar_linea_horizontal(self, h):
        y = 80 - h * 80
        self.pizarra.linea(-100, y, 100, y, self.pilas.colores.cyan, grosor=3)

    def pintar_linea_diagonal_1(self):
        self.pizarra.linea(-84, 84, 84, -84, self.pilas.colores.cyan, grosor=3)

    def pintar_linea_diagonal_2(self):
        self.pizarra.linea(84, 84, -84, -84, self.pilas.colores.cyan, grosor=3)

    def pintar_linea_vertical(self, v):
        x = -80 + v * 80
        self.pizarra.linea(x, -100, x, 100, self.pilas.colores.cyan, grosor=3)