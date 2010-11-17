import pilas
import sys

pilas.iniciar()

mono = pilas.actores.Mono()

bomba = pilas.actores.Bomba()
bomba.x = 200

banana = pilas.actores.Banana()
banana.x = -200

pilas.avisar("Mostrando tres actores de ejemplo.")
pilas.ejecutar()
