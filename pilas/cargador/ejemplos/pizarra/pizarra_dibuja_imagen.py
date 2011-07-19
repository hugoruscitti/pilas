import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
pizarra = pilas.actores.Pizarra()

imagen = pilas.imagenes.cargar("pelota.png")
pizarra.pintar_imagen(imagen, 0, 0)


pilas.avisar("Imprimiendo una imagen sobre la pizarra.")
pilas.ejecutar()
