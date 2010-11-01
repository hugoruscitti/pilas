import pilas
from PySFML import sf

pilas.iniciar(usar_motor='pygame')

mono = pilas.actores.Mono()

otro = mono.duplicar(y=-200)
pilas.avisar("Duplicando actores.")
pilas.ejecutar()
