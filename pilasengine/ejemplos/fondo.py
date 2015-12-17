import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas = pilasengine.iniciar()

fondo = pilas.fondos.Volley()

pilas.avisar("Un paisaje de ejemplo.")
pilas.ejecutar()
