import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
pizarra = pilas.actores.Pizarra()

pizarra.bajar_lapiz()

pizarra.mover_lapiz(100, 0)
pizarra.mover_lapiz(100, 100)
pizarra.mover_lapiz(0, 0)


#pilas.avisar("Una pizarra con algunas imagenes.")
pilas.ejecutar()
