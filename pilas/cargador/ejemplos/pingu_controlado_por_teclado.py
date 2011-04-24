import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
t = pilas.actores.Pingu()

pilas.avisar("Usa el teclado para mover al personaje (para arriba 'salta').")
pilas.ejecutar()
