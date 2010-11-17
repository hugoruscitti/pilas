import pilas
from PySFML import sf

pilas.iniciar()

mono = pilas.actores.Mono()

otro = mono.duplicar(y=-150)
pilas.avisar("Duplicando actores.")
pilas.ejecutar()
