import pilas
from PySFML import sf

pilas.iniciar()

tortuga = pilas.actores.Tortuga()

otro = tortuga.duplicar(y=-200)
pilas.avisar("Duplicando actores.")
pilas.ejecutar()
