import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas = pilasengine.iniciar()
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.Arrastrable)

pilas.avisar("Use el puntero del mouse para arrastrar al actor.")
pilas.ejecutar()
