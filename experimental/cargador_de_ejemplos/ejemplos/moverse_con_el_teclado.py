import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.MoverseConElTeclado)

pilas.avisar("Use los direccionales del teclado para mover al mono.")
pilas.ejecutar()
