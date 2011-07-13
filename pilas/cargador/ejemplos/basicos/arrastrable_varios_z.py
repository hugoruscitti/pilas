import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
mono1 = pilas.actores.Mono()
mono2 = pilas.actores.Mono()

mono2.escala = 2
mono2.z = 100


mono1.aprender(pilas.habilidades.Arrastrable)

pilas.avisar("Hay dos actores, uno se puede arrastrar con el mouse.")
pilas.ejecutar()
