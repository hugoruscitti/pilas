import pilasengine
from pilasengine.actores.bomba import Bomba

class BombaConMovimiento(Bomba):

    def actualizar(self):
        self.x += 1
        self.y += 1

        if self.x > 320:
            self.x = -320

        if self.y > 240:
            self.y = -240


pilas = pilasengine.iniciar()

protagonista = pilas.actores.Aceituna()
protagonista.aprender(pilas.habilidades.SeguirAlMouse)
pilas.ocultar_puntero_del_mouse()

bomba_1 = BombaConMovimiento(pilas)
bomba_2 = BombaConMovimiento(pilas, x=200, y=0)
bomba_3 = BombaConMovimiento(pilas, x=0, y=200)

pilas.ejecutar()
