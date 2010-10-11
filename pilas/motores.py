import pygame
from PySFML import sf
from pilas.simbolos import *

class Pygame:

    def __init__(self):
        pygame.init()

    def crear_ventana(self, ancho, alto, titulo):
        return pygame.display.set_mode((ancho, alto))



class pySFML:

    def __init__(self):
        pass

    def crear_ventana(self, ancho, alto, titulo):
        ventana = sf.RenderWindow(sf.VideoMode(ancho, alto), titulo)
        # Define que la coordenada (0, 0) sea el centro de la ventana.
        view = ventana.GetDefaultView()
        view.SetCenter(0, 0)
        self.input = ventana.GetInput()
        return ventana

    def pulsa_tecla(self, tecla):
        "Indica si una tecla esta siendo pulsada en este instante."

        mapa = {
                IZQUIERDA: sf.Key.Left,
                DERECHA: sf.Key.Right,
                ARRIBA: sf.Key.Up,
                ABAJO: sf.Key.Down,
                BOTON: sf.Key.Space,
                }

        return self.input.IsKeyDown(mapa[tecla])
