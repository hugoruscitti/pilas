import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

grupo = pilas.atajos.fabricar(pilas.actores.Mono, 20)
grupo.aprender(pilas.habilidades.RebotarComoPelota)
grupo.sonreir()
pilas.ejecutar()

