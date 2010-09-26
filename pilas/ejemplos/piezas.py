import pilas
import random

FILAS = 4
COLUMNAS = 4

class Piezas(pilas.escenas.Normal):

    def __init__(self):
        pilas.escenas.Normal.__init__(self, pilas.colores.gris_oscuro)
        grilla = pilas.imagenes.Grilla("ejemplos/data/piezas.png", FILAS, COLUMNAS)

        for x in range(FILAS * COLUMNAS):
            pieza = Pieza(grilla, x)
            pieza.x = random.randint(-200, 200)
            pieza.y = random.randint(-200, 200)

class Pieza(pilas.actores.Animacion):
    "Representa una pieza del rompecabezas."

    def __init__(self, grilla, cuadro):
        pilas.actores.Animacion.__init__(self, grilla)
        self.aprender(pilas.habilidades.Arrastrable)
        self.definir_cuadro(cuadro)

    def actualizar(self):
        pass

    def cuando_se_hace_click(self, **k):
        print "hacen click."
