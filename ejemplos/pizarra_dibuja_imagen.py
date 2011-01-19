import pilas
import sys

pilas.iniciar()
pizarra = pilas.actores.Pizarra()

imagen = pilas.imagenes.cargar("pelota.png")
pizarra.pintar_imagen(imagen, 0, 0)


pilas.ejecutar()
