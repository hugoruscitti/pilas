import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()

mono = pilas.actores.Mono()

otro = mono.duplicar(y=-150)
pilas.avisar("Duplicando actores.")
pilas.ejecutar()
