import pilas
import sys

pilas.iniciar(titulo='arrastrable')
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.Arrastrable)

pilas.ejecutar()
