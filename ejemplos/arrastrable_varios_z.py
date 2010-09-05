import pilas
import sys

pilas.iniciar()
mono1 = pilas.actores.Mono()
mono2 = pilas.actores.Mono()

mono2.escala = 2
mono2.z = 100


mono1.aprender(pilas.habilidades.Arrastrable)

pilas.ejecutar()
