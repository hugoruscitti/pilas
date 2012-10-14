# -*- encoding: utf-8 -*-
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

import pilas

pilas.iniciar(ancho=624, alto=480, sonido='deshabilitado')

class Pastilla(pilas.actores.Actor):

    def __init__(self, x, y):
        x-=12
        y-=12
        pilas.actores.Actor.__init__(self, "pastilla_1.png", x, y)
        self.radio_de_colision = 5


class Pacman(pilas.actores.Pacman):

    def __init__(self, mapa):
        self.mapa = mapa
        pilas.actores.Pacman.__init__(self, -12, -12)

    def actualizar(self):

        if self.control.izquierda:
            self.posicion = 0
        elif self.control.derecha:
            self.posicion = 1
        elif self.control.abajo:
            self.posicion = 3
        elif self.control.arriba:
            self.posicion = 2

        if self.posicion == 0:
            self.mover(-1, 0)
        elif self.posicion == 1:
            self.mover(1, 0)
        elif self.posicion == 2:
            self.mover(0, 1)
        elif self.posicion == 3:
            self.mover(0, -1)

    def mover(self, x, y):
        destino_x = x + self.velocidad * x
        destino_y = y + self.velocidad * y

        va_a_pisar_solido = self.mapa.es_punto_solido(destino_x, destino_y)

        if not va_a_pisar_solido:
            self._reproducir_animacion()
            self.x += self.velocidad * x
            self.y += self.velocidad * y



pilas.fondos.Color(pilas.colores.negro)
mapa = pilas.actores.MapaTiled('tile_pacman.tmx')
pacman = Pacman(mapa)
pacman.radio_de_colision = 5
pacman.escala = 2

pastillas = []


# Genera todas las pastillas de la tercer capa.
for (y, fila) in enumerate(mapa.capas[2]):
    for (x, bloque) in enumerate(fila):
        if bloque == 35:
            pastillas.append(Pastilla(x * 24 - 288, -y * 24 + 240))

def cuando_come_pastilla(pacman, pastilla):
    pastilla.eliminar()

pilas.escena_actual().colisiones.agregar(pacman, pastillas, cuando_come_pastilla)

#b = pilas.actores.Pingu()
pilas.ejecutar()
