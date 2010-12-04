import pilas
import sys

pilas.iniciar(usar_motor='pygame')
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.Arrastrable)

pilas.avisar("Use el puntero del mouse para arrastrar al actor (pygame).")
pilas.ejecutar()
