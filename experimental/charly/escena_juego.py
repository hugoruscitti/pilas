import pilas
import random
import protagonista
import pelota


class EscenaJuego(pilas.escenas.Escena):
    "Es la escena que permite controlar al pinguino y jugar"

    def __init__(self):
        pilas.escenas.Escena.__init__(self)
        self.puntaje = pilas.actores.Puntaje(x=280, y=220, color=pilas.colores.blanco)
        self.actores = []
        pilas.fondos.Tarde()
        self.pelotas = []
        self.protagonista = protagonista.Protagonista(self.pelotas)
        self.pelotas.append(pelota.Pelota())
        
        self.pelotas.append(pelota.Pelota(100, escala=3))
        self.pelotas.append(pelota.Pelota(200, escala=2))