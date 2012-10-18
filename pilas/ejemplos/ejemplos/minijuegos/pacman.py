# -*- encoding: utf-8 -*-
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

import pilas

pilas.iniciar(ancho=624, alto=480, audio='phonon')

class Pastilla(pilas.actores.Actor):

    def __init__(self, x, y):
        pilas.actores.Actor.__init__(self, "pastilla_1.png", x - 12, y - 12)
        self.radio_de_colision = 5


class Pacman(pilas.actores.Pacman):

    def __init__(self, mapa):
        self.mapa = mapa
        pilas.actores.Pacman.__init__(self, -12, -12)

    def actualizar(self):

        if self.control.izquierda:
            self.posicion = 0
            self.y = self.ajustar_coordenada_a_grilla(self.y)
        elif self.control.derecha:
            self.posicion = 1
            self.y = self.ajustar_coordenada_a_grilla(self.y)
        elif self.control.abajo:
            self.posicion = 3
            self.x = self.ajustar_coordenada_a_grilla(self.x)
        elif self.control.arriba:
            self.posicion = 2
            self.x = self.ajustar_coordenada_a_grilla(self.x)

        if self.posicion == 0:
            self.mover(-1, 0)
        elif self.posicion == 1:
            self.mover(1, 0)
        elif self.posicion == 2:
            self.mover(0, 1)
        elif self.posicion == 3:
            self.mover(0, -1)

    def mover(self, x, y):
        if x and y:
            raise Exception("El pacman no se puede mover en diagonal")

        destino_x = self.x + self.velocidad * x
        destino_y = self.y + self.velocidad * y
        dx = 0
        dy = 0

        if x:
            if x > 0:
                dx = 12
            else:
                dx = -12

            va_a_pisar_solido = self.mapa.es_punto_solido(destino_x + dx, self.y)

        if y:
            if y > 0:
                dy = 12
            else:
                dy = -12

            va_a_pisar_solido = self.mapa.es_punto_solido(self.x, self.y + dy)

        if not va_a_pisar_solido:
            self._reproducir_animacion()
            self.x += self.velocidad * x
            self.y += self.velocidad * y
        else:
            self.x = self.ajustar_coordenada_a_grilla(self.x)
            self.y = self.ajustar_coordenada_a_grilla(self.y)

    """
    def posicion_en_mapa(self):
        x, y = self.mapa.convertir_de_coordenada_absoluta_a_coordenada_mapa(self.x, self.y)
        fila = self.mapa.obtener_numero_de_fila(y)
        columna = self.mapa.obtener_numero_de_columna(x)
        return {'fila': fila, 'columna': columna}
    """

    def ajustar_coordenada_a_grilla(self, coordenada):
        return (int(coordenada / 24) * 24) + 12


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
