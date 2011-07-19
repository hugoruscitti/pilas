import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
pizarra = pilas.actores.Pizarra()

pizarra.linea(0, 0, 100, 0, grosor=2)
pizarra.linea(100, 0, 100, 100, grosor=2)
pizarra.linea(100, 100, 0, 0, grosor=2)


pilas.avisar("Una pizarra con algunas lineas.")
pilas.ejecutar()
