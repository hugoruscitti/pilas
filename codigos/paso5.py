import pilas
import bombaconmovimiento
import aceituna


def cuando_colisionan(aceituna, bomba):
    bomba.explotar()

pilas.iniciar(gravedad=(0,0))

protagonista = aceituna.Aceituna()

bomba_1 = bombaconmovimiento.BombaConMovimiento()
bomba_2 = bombaconmovimiento.BombaConMovimiento(x=200, y=0)
bomba_3 = bombaconmovimiento.BombaConMovimiento(x=0, y=200)

lista_de_bombas = [bomba_1, bomba_2, bomba_3]

pilas.mundo.colisiones.agregar(protagonista, lista_de_bombas, cuando_colisionan)

pilas.ejecutar()
