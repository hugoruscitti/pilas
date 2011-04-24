import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar(usar_motor='pygame')
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.Arrastrable)

pilas.avisar("Use el puntero del mouse para arrastrar al actor (pygame).")
pilas.ejecutar()
