import pilas
import sys

pilas.iniciar()
pizarra = pilas.actores.Pizarra()

grilla = pilas.imagenes.Grilla("pingu.png", 10)
pizarra.pintar_grilla(grilla, 0, 0)

grilla.definir_cuadro(2)
pizarra.pintar_grilla(grilla, 100, 100)

grilla.definir_cuadro(3)
pizarra.pintar_grilla(grilla, 200, 200)

pilas.ejecutar()
