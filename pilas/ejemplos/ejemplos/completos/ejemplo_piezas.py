# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

import pilas

pilas.iniciar()
pilas.cambiar_escena(pilas.demos.piezas.Piezas())
pilas.ejecutar()
