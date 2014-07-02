import pilasengine
from pilasengine.actores.bomba import Bomba

class BombaConMovimiento(Bomba):

    def iniciar(self):
        self.circulo = pilas.fisica.Circulo(self.x, self.y, 20, restitucion=1, friccion=0, amortiguacion=0)
        self.imitar(self.circulo)

        self._empujar()

    def _empujar(self):
        self.circulo.impulsar(2, 2)


def cuando_colisionan(aceituna, bomba):
    bomba.explotar()

pilas = pilasengine.iniciar(gravedad=(0,0))

protagonista = pilas.actores.Aceituna()
protagonista.aprender(pilas.habilidades.SeguirAlMouse)
pilas.mundo.motor.ocultar_puntero_del_mouse()

bomba_1 = BombaConMovimiento(pilas)
bomba_2 = BombaConMovimiento(pilas, x=200, y=0)
bomba_3 = BombaConMovimiento(x=0, y=200)

lista_de_bombas = [bomba_1, bomba_2, bomba_3]

pilas.mundo.colisiones.agregar(protagonista, lista_de_bombas, cuando_colisionan)

pilas.ejecutar()
