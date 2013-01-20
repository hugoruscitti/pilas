import pilas
from pilas.actores import Bomba

class BombaConMovimiento(Bomba):

    def __init__(self, x=0, y=0):
        Bomba.__init__(self, x, y)

        self.circulo = pilas.fisica.Circulo(x, y, 20, restitucion=1, friccion=0, amortiguacion=0)
        self.imitar(self.circulo)

        self._empujar()

    def _empujar(self):
        dx = 1
        dy = 1
        self.circulo.impulsar(dx * 10, dy * 10)
